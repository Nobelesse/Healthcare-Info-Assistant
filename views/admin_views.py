"""Consent-gated admin panels with fully localized interface text."""
import plotly.graph_objects as go
import streamlit as st
from database import store
from ui.components import section, metric
from ui.strings import t, event_label
from views.user_views import when, _labs_dataframe, _chart_theme


def overview(admin,lang):
    section(t('admin_overview',lang),t('admin_overview_desc',lang),t('admin_overline',lang))
    numbers=store.counts()
    summary=store.admin_user_insights(admin['id'])
    for col,(key,value,icon) in zip(st.columns(4),[
        ('admin_registered',numbers['users'],'👥'),('admin_convos',numbers['questions'],'💬'),
        ('admin_analyzed',numbers['reports'],'📄'),('admin_voice',numbers['voice'],'🎙')]):
        with col: metric(t(key,lang),str(value),icon)
    st.markdown('<div class="glass-panel"><b>🛡️ '+t('admin_privacy_title',lang)+'</b><p>'+t('admin_privacy_desc',lang)+'</p></div>',unsafe_allow_html=True)
    a,b=st.columns([1,1.3])
    with a:
        st.markdown('#### '+t('admin_account_status',lang))
        fig=go.Figure(go.Pie(labels=[t('admin_active',lang),t('admin_inactive',lang)],
                             values=[summary.get('active',0),summary.get('inactive',0)],
                             hole=.68,marker=dict(colors=['#18a697','#e6a66e'])))
        theme=_chart_theme(lang)
        fig.update_layout(height=260,margin=dict(l=10,r=10,t=10,b=10),
                          paper_bgcolor=theme['paper_bgcolor'],font_color=theme['font_color'],
                          legend=dict(orientation='h',y=-.1))
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})
    with b:
        st.markdown('#### '+t('admin_recent',lang))
        recent=store.list_users()[:10]
        if recent:
            st.dataframe([{t('field_username',lang):u['username'],
                           t('admin_active',lang):u['is_active'],
                           t('admin_joined',lang):when(u['created_at'])} for u in recent],
                         hide_index=True,width='stretch')
        else: st.info(t('admin_no_users',lang))
        st.caption(t('admin_directory_tip',lang))


def users(admin,lang):
    section(t('admin_user_directory',lang),t('admin_user_directory_desc',lang),t('admin_directory_overline',lang))
    term=st.text_input(t('admin_search',lang),placeholder=t('admin_search_hint',lang))
    found=store.list_users(term)
    st.caption(t('admin_found',lang,count=len(found)))
    for user in found[:80]:
        uid=user['id']
        with st.expander(f'{"🟢" if user["is_active"] else "🔴"} @{user["username"]} · #{uid}'):
            if st.button(t('admin_view_profile',lang),key=f'profile_{uid}'):
                store.record_audit(admin['id'],'admin_read_user_profile',uid)
                st.session_state[f'admin_profile_{uid}']=True
            if st.session_state.get(f'admin_profile_{uid}'):
                st.write(f'**{t("field_full_name",lang)}:** {user["full_name"]}')
                st.write(f'**{t("field_email",lang)}:** {user["email"]}')
                st.write(f'**{t("admin_preferred_lang",lang)}:** {user["language"].upper()}')
                st.write(f'**{t("admin_consent",lang)}:** {t("admin_yes",lang) if user["consented"] else t("admin_no",lang)}')
                st.write(f'**{t("admin_joined",lang)}:** {when(user["created_at"])}')
                st.write(f'**{t("admin_last_login",lang)}:** {when(user["last_login_at"])}')
            st.write(f'**{t("admin_account",lang)}:** {t("admin_active",lang) if user["is_active"] else t("admin_disabled",lang)}')
            if st.button(t('admin_deactivate',lang) if user['is_active'] else t('admin_reactivate',lang),
                         key=f'status_{uid}'):
                if store.set_user_active(uid,not user['is_active']):
                    store.record_audit(admin['id'],'admin_user_status_change',uid)
                    st.rerun()


def reports(admin,lang):
    section(t('admin_reports_title',lang),t('admin_reports_desc',lang),t('admin_sensitive_reports',lang))
    entries=store.admin_report_headers(admin['id'])
    if not entries: st.info(t('admin_no_reports',lang));return
    for entry in entries:
        rid=entry['id']
        header=t('admin_report_header',lang,id=rid,user=entry['user_id'],date=when(entry['created_at']))
        with st.expander('📄 '+header):
            st.caption(t('admin_report_pages',lang,pages=entry['page_count']))
            if st.button('🔒 '+t('admin_open_report',lang),key=f'admin_report_{rid}'):
                detail=store.admin_open_report(admin['id'],rid)
                if detail: st.session_state[f'admin_open_report_{rid}']=detail
                else: st.error(t('admin_no_consent',lang))
            detail=st.session_state.get(f'admin_open_report_{rid}')
            if detail:
                st.write(f'**{t("admin_file",lang)}:** {detail["filename"]}')
                _labs_dataframe(detail['labs'],lang)
                st.markdown(detail['ai_summary'])
                with st.expander(t('admin_extracted',lang)):
                    st.text(detail['extracted_text'])


def conversations(admin,lang):
    section(t('admin_convos_title',lang),t('admin_convos_desc',lang),t('admin_sensitive_chat',lang))
    entries=store.admin_conversation_headers(admin['id'])
    if not entries: st.info(t('admin_no_convos',lang));return
    for entry in entries:
        cid=entry['id']
        label=t('admin_chat_header',lang,id=cid,user=entry['user_id'],date=when(entry['created_at']))
        with st.expander(('🎙 ' if entry['kind']=='voice' else '💬 ')+label):
            if st.button('🔒 '+t('admin_open_chat',lang),key=f'admin_chat_{cid}'):
                detail=store.admin_open_conversation(admin['id'],cid)
                if detail: st.session_state[f'admin_open_chat_{cid}']=detail
                else: st.error(t('admin_no_consent',lang))
            detail=st.session_state.get(f'admin_open_chat_{cid}')
            if detail:
                st.markdown('**'+t('history_question',lang)+'**');st.write(detail['question'])
                st.markdown('**'+t('history_answer',lang)+'**');st.markdown(detail['response'])


def audit(admin,lang):
    section(t('admin_audit_title',lang),t('admin_audit_desc',lang),t('admin_audit_overline',lang))
    rows=store.audit_log(limit=200)
    if not rows: st.info(t('admin_no_audit',lang));return
    actions=sorted({r['action'] for r in rows})
    selection=st.selectbox(t('admin_filter',lang),['all']+actions,
                           format_func=lambda v:t('admin_all',lang) if v=='all' else event_label(v,lang))
    filtered=[r for r in rows if selection=='all' or r['action']==selection]
    st.dataframe([{t('admin_time',lang):when(x['created_at']),
                   t('admin_actor',lang):x['actor_id'],t('admin_action',lang):event_label(x['action'],lang),
                   t('admin_user_id',lang):x['target_user_id'],t('admin_record_id',lang):x['target_id']}
                  for x in filtered],hide_index=True,width='stretch')
    st.caption(t('admin_audit_note',lang))
