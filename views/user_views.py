"""Member-facing views with complete static UI localization."""
from collections import Counter
from datetime import datetime
from html import escape
import hashlib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from auth.service import AuthError, change_password, confirm_password
from config.settings import MAX_REPORT_BYTES, ENABLE_OCR
from database import store
from services.ollama_service import medical_answer, report_answer, emergency_notice, OllamaUnavailable, check_ollama
from services.report_service import extract_pdf, extract_image, analyze_labs, ReportError, clean_filename
from services.voice_service import transcribe_audio_with_language, VoiceError
from services.translation_service import display_in_language, preferred_voice_language, voice_display_language
from services.session_flow import active_chat, claim_recording
from services.export_service import make_english_pdf
from services.knowledge_service import search_knowledge
from services.comparison_service import compare_reports
from services.offline_status import inspect_offline
from ui.v2_strings import v2t
from ui.components import hero, section, metric, feature_card, advisory, speech_button
from ui.strings import t, local_status, LANGUAGES, complete_locales


def when(value):
    return value.strftime('%Y-%m-%d %H:%M') if isinstance(value,datetime) else '—'


def ai_status():
    @st.cache_data(ttl=18, show_spinner=False)
    def _status():
        return check_ollama()
    return _status()


def _navigate(page):
    st.session_state.page=page
    st.rerun()


def _chart_theme(lang):
    light=st.session_state.get('theme','dark')=='light'
    return {'font_color':'#244654' if light else '#c9e5ed',
            'paper_bgcolor':'rgba(0,0,0,0)','plot_bgcolor':'rgba(0,0,0,0)'}


def dashboard(user,lang):
    hero(user['full_name'].split()[0],lang)
    st.write('')
    counts=store.counts(user['id'])
    stats=[('dash_stats_chat',counts['questions'],'💬'),('dash_stats_reports',counts['reports'],'📄'),
           ('dash_stats_voice',counts['voice'],'🎙'),('dash_stats_model','Llama 3.2','✧')]
    for col,(key,value,icon) in zip(st.columns(4),stats):
        with col: metric(t(key,lang),value,icon)
    st.write('')
    section(t('dash_heading',lang),t('dash_desc',lang),t('sidebar_workspace',lang))
    features=[('chat','chat','dash_chat_desc','🧠'),('reports','reports','dash_reports_desc','📋'),
              ('voice','voice','dash_voice_desc','🎙'),('insights','insights','dash_insights_desc','📊')]
    # Keep the four interactive actions in a dedicated, CSS-scoped grid. Card
    # heights and button alignment are shared across all translations, without
    # changing the reusable feature cards on the About page.
    with st.container(key='dashboard_quick_actions'):
        for col,(page,key,desc,icon) in zip(st.columns(4, gap='medium'),features):
            with col:
                feature_card(t(key,lang),t(desc,lang),icon)
                if st.button(t('action_open',lang),key='quick_'+page,width='stretch'):
                    _navigate(page)
    ok,label=ai_status()
    (st.success if ok else st.warning)(("🟢 " + t('ollama_ready',lang)) if ok else
                                       ("🟠 " + t('ollama_offline',lang)))
    parts=''.join(f'<span><b>{i:02d}</b> {escape(t(key,lang))}</span>' +
                  ('<i>→</i>' if i<4 else '') for i,key in enumerate(
                  ('journey_1','journey_2','journey_3','journey_4'),start=1))
    st.markdown(f'<div class="journey-panel"><div class="journey-label">{escape(t("journey",lang))}</div>'
                f'<div class="journey-steps">{parts}</div></div>', unsafe_allow_html=True)
    advisory(lang)


def chat(user,lang):
    section(t('chat',lang),t('chat_desc',lang),t('chat_overline',lang))
    advisory(lang)
    a,b=st.columns(2)
    with a:
        detail=st.select_slider(t('chat_detail',lang),options=['short','standard','detailed'],
                                value='standard',format_func=lambda code:t('detail_'+code,lang))
    with b:
        diet=st.checkbox(t('chat_vegetarian',lang))
    # Do NOT load saved records into the open chat. The History page remains the
    # only place where earlier logins' conversations are displayed.
    medical=active_chat(st.session_state,user['id'])
    if not medical: st.info(t('chat_try',lang))
    localized_last = None
    for item in medical[-12:]:
        with st.chat_message('user',avatar='👤'): st.markdown(item['question'])
        display_answer, translated = display_in_language(
            st.session_state, item['response'], lang, item.get('language'), user['id'])
        with st.chat_message('assistant',avatar='🩺'):
            if not translated: st.caption('🌐 '+t('translation_unavailable',lang))
            st.markdown(display_answer)
        notes=search_knowledge(item['question'])
        if notes:
            with st.expander('📚 '+v2t('sources',lang)):
                st.caption(v2t('source_note',lang))
                for source in notes:
                    st.markdown(f'**{source["title"]}** — {source["source_title"]}')
                    if lang=='en': st.caption(source['summary'])
                    st.caption(source['source_url'])
        localized_last = (display_answer, translated)
    if localized_last:
        # Speak the language of the DISPLAYED text, never an old English reply.
        if localized_last[1]: speech_button(localized_last[0], lang, key='chat_tts')
    prompt=st.chat_input(t('chat_placeholder',lang))
    if prompt:
        urgent=emergency_notice(prompt,lang)
        if urgent:
            store.save_interaction(user['id'],prompt,urgent)
            medical.append({'question':prompt,'response':urgent,'language':lang})
            st.rerun()
        try:
            # Stream only the current reply; previous private chat remains user-session scoped.
            with st.chat_message('assistant',avatar='🩺'):
                response=st.write_stream(medical_answer(prompt,lang,medical,detail,
                    'vegetarian' if diet else 'any',stream=True))
            store.save_interaction(user['id'],prompt,response)
            medical.append({'question':prompt,'response':response,'language':lang})
            st.rerun()
        except (OllamaUnavailable,ValueError):
            st.error(t('generic_error',lang))
    st.caption(t('chat_disclaimer',lang))


def _labs_dataframe(labs,lang='en'):
    if not labs:
        st.info(t('lab_none',lang));return
    df=pd.DataFrame(labs)[['name','value','unit','reference','status']]
    df.columns=[t('lab_col_'+key,lang) for key in ('name','result','unit','range','comparison')]
    df.iloc[:,-1]=df.iloc[:,-1].map(lambda value:local_status(value,lang))
    st.dataframe(df,hide_index=True,width='stretch')
    flags=Counter(item.get('status','Not evaluated') for item in labs)
    labels=[('status_in','Within stated range','✓'),('status_high','High','↑'),
            ('status_low','Low','↓'),('status_uneval','Not evaluated','?')]
    for col,(key,status,icon) in zip(st.columns(4),labels):
        with col: metric(t(key,lang),flags[status],icon)
    st.caption(t('lab_verify',lang))


def _report_export(report,lang,prefix='my',localized_summary=None):
    chosen_summary = report['ai_summary'] if localized_summary is None else localized_summary
    text_data=f'Healthcare Info Assistant\n{t("reports",lang)}: {report["filename"]}\n\n{chosen_summary}\n\n{t("export_disclaimer",lang)}'
    st.download_button('⬇ '+t('export_txt',lang),text_data.encode('utf-8'),
                       f'{prefix}_report_{report["id"]}.txt',mime='text/plain',key=f'txt_{prefix}_{report["id"]}')
    if lang=='en':
        pdf=make_english_pdf(report['filename'],chosen_summary)
        st.download_button('⬇ '+t('export_pdf',lang),pdf,f'{prefix}_report_{report["id"]}.pdf',
                           mime='application/pdf',key=f'pdf_{prefix}_{report["id"]}')
    else:
        st.caption(t('export_note',lang))


def report_analyzer(user,lang):
    section(t('reports',lang),t('reports_desc',lang),t('reports_overline',lang))
    advisory(lang)
    st.markdown(f'<div class="glass-panel report-intro"><b>📄 {escape(t("reports_intro_title",lang))}</b>'
                f'<p>{escape(t("reports_intro_desc",lang))}</p></div>',unsafe_allow_html=True)
    upload=st.file_uploader(t('reports_upload',lang),type=['pdf','png','jpg','jpeg'],accept_multiple_files=False)
    st.caption(t('reports_consent_note',lang))
    if upload is not None:
        if upload.size>MAX_REPORT_BYTES: st.error(t('reports_oversize',lang))
        else:
            image_needs_ocr = upload.name.lower().endswith(('.png','.jpg','.jpeg')) and not ENABLE_OCR
            if image_needs_ocr: st.warning(v2t('ocr_setup',lang))
            analyze_clicked = st.button('✦ '+t('reports_analyze',lang),type='primary',disabled=image_needs_ocr)
        if upload.size<=MAX_REPORT_BYTES and analyze_clicked:
            try:
                with st.spinner(t('reports_extracting',lang)):
                    if upload.name.lower().endswith('.pdf'):
                        extracted,pages=extract_pdf(upload.getvalue())
                    else:
                        extracted,pages=extract_image(upload.getvalue())
                    labs=analyze_labs(extracted)
                st.success(t('reports_parsed',lang,pages=pages,count=len(labs)))
                _labs_dataframe(labs,lang)
                with st.spinner(t('reports_generating',lang)):
                    summary=report_answer(extracted,labs,lang)
                report_id=store.save_report(user['id'],clean_filename(upload.name),pages,extracted,labs,summary)
                st.session_state.last_report_id=report_id
                st.session_state.setdefault('report_original_languages',{})[report_id]=lang
                st.success(t('reports_saved',lang))
            except (ReportError,OllamaUnavailable,ValueError) as exc: st.error(t("generic_error",lang))
    reports=store.list_reports(user['id'],limit=20)
    if reports:
        st.write('')
        section(t('reports_saved_title',lang),t('reports_saved_desc',lang),t('reports_library',lang))
        ids={f'#{r["id"]} · {r["filename"]} · {when(r["created_at"])}':r['id'] for r in reports}
        selected=st.selectbox(t('reports_select',lang),list(ids))
        if selected:
            report=store.get_report(ids[selected],user['id'])
            if report:
                _labs_dataframe(report['labs'],lang)
                summary, translated = display_in_language(
                    st.session_state, report['ai_summary'], lang,
                    st.session_state.get('report_original_languages',{}).get(report['id']), user['id'])
                if not translated: st.warning(t('translation_unavailable',lang))
                st.markdown(summary)
                if translated: speech_button(summary,lang,key='report_tts')
                _report_export(report,lang,localized_summary=summary)
                with st.expander(t('reports_source',lang)):
                    st.text(report['extracted_text'])
                with st.expander(t('reports_delete',lang)):
                    st.warning(t('reports_delete_warning',lang))
                    if st.button(t('reports_delete_confirm',lang),key=f'del_r_{report["id"]}'):
                        store.delete_report(user['id'],report['id']);st.rerun()


def _send_voice_query(user, lang, question, answer_lang=None):
    """Persist recognized speech once, answering in the detected speaking language."""
    reply_lang=answer_lang or lang
    question=question.strip()
    if not question:
        return False
    urgent=emergency_notice(question,reply_lang)
    if urgent:
        store.save_interaction(user['id'],question,urgent,kind='voice')
        st.session_state['last_voice_response']=urgent
        st.session_state['last_voice_response_lang']=reply_lang
        st.session_state['voice_response_revision']=st.session_state.get('language_revision',0)
        st.session_state['voice_submitted_text']=question
        return True
    try:
        with st.spinner(t('voice_generating',lang)):
            result=medical_answer(question,reply_lang)
        store.save_interaction(user['id'],question,result,kind='voice')
        st.session_state['last_voice_response']=result
        st.session_state['last_voice_response_lang']=reply_lang
        st.session_state['voice_response_revision']=st.session_state.get('language_revision',0)
        st.session_state['voice_submitted_text']=question
        return True
    except (ValueError,OllamaUnavailable):
        st.error(t('generic_error',lang))
        return False


def voice_assistant(user,lang):
    section(t('voice',lang),t('voice_desc',lang),t('voice_overline',lang))
    st.markdown('''<div class="voice-scene" role="img" aria-label="AI voice assistant microphone visual">
        <div class="voice-ring"></div><div class="voice-ring r2"></div><div class="voice-ring r3"></div>
        <div class="voice-orb"><svg class="voice-mic-icon" viewBox="0 0 100 100" fill="none"
        xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect x="33" y="15" width="34" height="51" rx="17" fill="url(#micBody)" stroke="#E9FFFC" stroke-width="4"/>
        <path d="M23 48v6c0 15 12 27 27 27s27-12 27-27v-6" stroke="#E9FFFC" stroke-width="6" stroke-linecap="round"/>
        <path d="M50 81v12M34 94h32" stroke="#E9FFFC" stroke-width="5" stroke-linecap="round"/>
        <path d="M42 29h16M42 39h16" stroke="#C6FFF6" stroke-width="3" stroke-linecap="round" opacity=".8"/>
        <defs><linearGradient id="micBody" x1="29" y1="17" x2="70" y2="66" gradientUnits="userSpaceOnUse">
        <stop stop-color="#9EFFF1"/><stop offset=".5" stop-color="#38DDDA"/><stop offset="1" stop-color="#126C9C"/>
        </linearGradient></defs></svg></div></div>''',unsafe_allow_html=True)
    st.caption(t('voice_permission',lang))
    # st.audio_input reruns on completed recording; no separate Ask click needed.
    recording=st.audio_input(t('voice_record',lang),sample_rate=16000,key='voice_record_widget')
    detect=st.checkbox(t('voice_detect',lang),value=True)
    if recording is not None:
        audio=recording.getvalue()
        digest=hashlib.sha256(audio).hexdigest() if audio else ''
        if claim_recording(st.session_state,digest):
            # Drop the last displayed result when a DIFFERENT clip is recorded.
            st.session_state.pop('last_voice_response',None)
            st.session_state['voice_submitted_text']=''
            st.session_state['voice_transcript']=''
            st.session_state['voice_record_digest']=digest
            try:
                with st.spinner(t('voice_transcribing',lang)):
                    transcript, spoken_code = transcribe_audio_with_language(audio,None if detect else lang)
                if transcript.strip():
                    st.session_state['voice_transcript']=transcript.strip()
                    reply_lang = preferred_voice_language(lang, spoken_code, detect, LANGUAGES)
                    st.session_state['voice_detected_language']=reply_lang
                    # Auto-dispatch in the actual spoken language, not the UI locale.
                    _send_voice_query(user,lang,transcript,answer_lang=reply_lang)
                else:
                    st.error(t('generic_error',lang))
            except VoiceError:
                st.error(t('generic_error',lang))
        if st.session_state.get('voice_record_digest') == digest and st.session_state.get('voice_transcript'):
            # Optional correction only: the FIRST answer was already sent.
            corrected=st.text_area(t('voice_review',lang),
                                    value=st.session_state['voice_transcript'],
                                    key='edit_transcript_'+digest[:30],height=100)
            detected_code=st.session_state.get('voice_detected_language',lang)
            st.caption(t('voice_detected_language',lang,locale=LANGUAGES.get(detected_code,detected_code)))
            st.caption(t('voice_review_note',lang))
            if corrected.strip() and corrected.strip()!=st.session_state.get('voice_submitted_text',''):
                if st.button('✦ '+t('voice_ask',lang),type='secondary',key='voice_corrected_submit'):
                    _send_voice_query(user,lang,corrected,
                                      answer_lang=st.session_state.get('voice_detected_language',lang))
        # A rerun from any other widget will NOT send the same recording again.
    if st.session_state.get('last_voice_response'):
        st.markdown('### 🩺 '+t('voice_response',lang))
        original_lang = st.session_state.get('last_voice_response_lang',lang)
        display_lang = voice_display_language(
            lang, original_lang, st.session_state.get('language_revision',0),
            st.session_state.get('voice_response_revision',0))
        answer, translated = display_in_language(
            st.session_state,st.session_state['last_voice_response'],display_lang,original_lang,user['id'])
        if not translated: st.warning(t('translation_unavailable',lang))
        st.markdown(answer)
        if translated: speech_button(answer,display_lang,key='voice_tts')
    advisory(lang)


def history(user,lang):
    section(t('history',lang),t('history_desc',lang),t('history_overline',lang))
    interactions=store.list_interactions(user['id'],limit=100)
    if not interactions: st.info(t('empty',lang));return
    filters=['all','medical','voice']
    selection=st.selectbox(t('history_type',lang),filters,
                           format_func=lambda x:t('history_'+x,lang))
    # Select ONE saved conversation at a time. Auto-translating 100 medical
    # answers on a laptop would block the page for minutes and waste resources.
    visible=[item for item in interactions if selection=='all' or item['kind']==selection]
    if not visible: st.info(t('empty',lang));return
    current=st.selectbox(
        t('history_choose',lang),range(len(visible)),
        format_func=lambda index: (
            f'{"🎙" if visible[index]["kind"]=="voice" else "💬"} '
            f'{visible[index]["question"][:90]} · {when(visible[index]["created_at"])}'),
        key='history_selected_item')
    item=visible[current]
    with st.container(border=True):
        st.markdown('**'+t('history_question',lang)+'**');st.write(item['question'])
        st.markdown('**'+t('history_answer',lang)+'**')
        localized, translated = display_in_language(
            st.session_state,item['response'],lang,None,user['id'])
        if not translated: st.caption('🌐 '+t('translation_unavailable',lang))
        st.markdown(localized)
        if translated: speech_button(localized,lang,key=f'history_tts_{item["id"]}')
        if st.button('🗑 '+t('action_delete',lang),key=f'del_chat_{item["id"]}'):
            store.delete_interaction(user['id'],item['id']);st.rerun()


def insights(user,lang):
    section(t('insights',lang),t('insights_desc',lang),t('insights_overline',lang))
    reports=store.list_reports(user['id'],limit=100)
    if not reports: st.info(t('insights_empty',lang));return
    labs=[lab for report in reports for lab in report['labs']]
    values=Counter(lab['status'] for lab in labs)
    for col,(key,val,icon) in zip(st.columns(3),[
            ('insights_saved',len(reports),'📄'),('insights_parsed',len(labs),'🔬'),
            ('insights_flags',values['Low']+values['High'],'⚑')]):
        with col: metric(t(key,lang),val,icon)
    if not labs: st.info(t('insights_no_labs',lang));return
    palette=_chart_theme(lang)
    a,b=st.columns(2)
    with a:
        fig=go.Figure(go.Pie(labels=[local_status(v,lang) for v in values],
                             values=list(values.values()),hole=.68,
                             marker={'colors':[{'High':'#ef944b','Low':'#e67791','Within stated range':'#159e92','Not evaluated':'#708da6'}.get(x,'#708da6') for x in values]}))
        fig.update_layout(title=t('insights_range_title',lang),height=360,
                          margin=dict(l=10,r=10,t=55,b=10),showlegend=True,
                          font_color=palette['font_color'],paper_bgcolor=palette['paper_bgcolor'],
                          legend=dict(orientation='h',y=-.1))
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})
    with b:
        common=Counter(x['name'] for x in labs).most_common(9)
        fig=go.Figure(go.Bar(x=[v for _,v in common],y=[k for k,_ in common],
                             orientation='h',marker={'color':'#16a598'}))
        fig.update_layout(title=t('insights_tests_title',lang),height=360,
                          margin=dict(l=10,r=10,t=55,b=10),
                          paper_bgcolor=palette['paper_bgcolor'],plot_bgcolor=palette['plot_bgcolor'],
                          font_color=palette['font_color'],xaxis_title=t('insights_count',lang),
                          yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})
    with st.expander(t('insights_compare',lang)):
        selected=st.selectbox(t('insights_test',lang),sorted({x['name'] for x in labs}))
        observations=[]
        for report in sorted(reports,key=lambda r:r['created_at']):
            for lab in report['labs']:
                if lab['name']==selected and isinstance(lab.get('value'),(int,float)):
                    observations.append((when(report['created_at']),lab['value'],lab['unit']))
        units={x[2] for x in observations}
        if len(units)!=1 or 'unit not found' in units: st.info(t('insights_units_warning',lang))
        elif len(observations)<2: st.info(t('insights_need_two',lang))
        else:
            fig=go.Figure(go.Scatter(x=[x[0] for x in observations],
                                     y=[x[1] for x in observations],mode='lines+markers',
                                     line={'color':'#14aa9e','width':3},marker={'size':9}))
            fig.update_layout(height=280,yaxis_title=next(iter(units)),**palette)
            st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})
            st.caption(t('insights_chart_note',lang))
    if len(reports) >= 2:
        with st.expander('📈 '+v2t('compare_heading',lang)):
            st.caption(v2t('compare_explain',lang))
            options=list(range(len(reports)))
            labels=lambda i:f'#{reports[i]["id"]} · {reports[i]["filename"]} · {when(reports[i]["created_at"])}'
            left,right=st.columns(2)
            with left:
                index_a=st.selectbox(v2t('earlier',lang),options,index=1,format_func=labels,key='v2_earlier')
            with right:
                index_b=st.selectbox(v2t('later',lang),options,index=0,format_func=labels,key='v2_later')
            if index_a==index_b:
                st.info(v2t('choose_distinct',lang))
            else:
                rows=compare_reports(reports[index_a],reports[index_b])
                if rows:
                    df=pd.DataFrame(rows)
                    df=df.rename(columns={'name':v2t('test',lang),'unit':v2t('unit',lang),
                         'earlier':v2t('earlier_result',lang),'later':v2t('later_result',lang),
                         'change':v2t('difference',lang),'earlier_status':v2t('earlier_status',lang),
                         'later_status':v2t('later_status',lang)})
                    st.dataframe(df,hide_index=True,width='stretch')
                    st.download_button('⬇ CSV',df.to_csv(index=False).encode('utf-8-sig'),
                        'healthcare_comparison.csv',mime='text/csv',key='v2_compare_csv')
                else:
                    st.info(v2t('no_comparable_tests',lang))
            st.caption(v2t('compare_warning',lang))
    st.warning(t('insights_warning',lang))


def offline_readiness(lang):
    section(v2t('offline_heading',lang),v2t('offline_intro',lang),'◉')
    status=inspect_offline()
    lines=[('local_ollama',status['ollama_local']),
           ('model_ready',status['ollama_model_ready']),
           ('knowledge_ready',status['knowledge_packaged']),
           ('whisper_ready',status['whisper_cache_detected'] and status['whisper_installed']),
           ('ocr_ready',status['ocr_enabled'] and status['tesseract_found'])]
    for key,ready in lines:
        st.markdown(('✅ ' if ready else '⚪ ')+v2t(key,lang))
    st.info(v2t('offline_disclaimer',lang))
    st.caption(status['ollama_message'])
    advisory(lang)


def profile(user,lang):
    section(t('profile',lang),t('profile_desc',lang),t('profile_overline',lang))
    st.markdown('### '+t('profile_details',lang))
    st.write(f'**{t("field_username",lang)}:** {user["username"]} · **{t("field_email",lang)}:** {user["email"]}')
    with st.form('profile_edit'):
        name=st.text_input(t('profile_display',lang),value=user['full_name'],max_chars=120)
        selection=st.selectbox(t('field_preferred_language',lang),complete_locales(),
                               index=complete_locales().index(user['language']) if user['language'] in complete_locales() else 0,
                               format_func=LANGUAGES.get)
        if st.form_submit_button(t('profile_save',lang)):
            if len(name.strip())<2: st.error(t('profile_short_name',lang))
            else:
                store.update_user_profile(user['id'],name.strip(),selection)
                st.session_state.language=selection;st.success(t('profile_updated',selection));st.rerun()
    with st.expander('🔐 '+t('profile_change_password',lang)):
        with st.form('change_pw'):
            old=st.text_input(t('profile_current_password',lang),type='password')
            new=st.text_input(t('profile_new_password',lang),type='password')
            if st.form_submit_button(t('profile_change_password',lang)):
                try:
                    if change_password(user['id'],old,new): st.success(t('profile_password_changed',lang))
                    else: st.error(t('profile_password_wrong',lang))
                except AuthError as exc: st.error(t("auth_password_error",lang))
    with st.expander('🗑 '+t('profile_delete',lang)):
        st.warning(t('profile_delete_warning',lang))
        with st.form('delete_my_account'):
            confirm=st.text_input(t('profile_confirm_type',lang))
            pw=st.text_input(t('profile_your_password',lang),type='password')
            if st.form_submit_button(t('profile_delete_submit',lang)):
                if confirm=='DELETE' and confirm_password(user['id'],pw):
                    store.delete_account(user['id']);st.session_state.clear();st.rerun()
                else: st.error(t('profile_delete_error',lang))
    advisory(lang)
