"""Responsive UI while the first offline translation pack is prepared."""
import streamlit as st

from services.locale_service import ensure_job, job_status, retry_job
from ui.strings import LANGUAGES, locale_coverage, reload_locale_cache
from ui.locale_wait_labels import message


def show_locale_preparation(lang: str):
    # Keep the language selector usable, including if a local Ollama instance
    # is offline. Do not render the old-language navigation/content meanwhile.
    with st.sidebar:
        st.markdown('**Healthcare Info Assistant**')
        if st.session_state.get('_pending_locale_last') != lang:
            st.session_state['_pending_locale_select'] = lang
            st.session_state['_pending_locale_last'] = lang
        selected = st.selectbox(
            message(lang, 'select'), options=list(LANGUAGES),
            format_func=LANGUAGES.get, key='_pending_locale_select',
            accept_new_options=False, width='stretch'
        )
        if selected != lang:
            st.session_state['language'] = selected
            st.session_state['language_revision'] = st.session_state.get('language_revision', 0) + 1
            st.rerun()

    st.title(message(lang, 'title'))
    st.info(message(lang, 'detail'))
    st.caption(message(lang, 'hint'))
    ensure_job(lang)

    # Fragment refresh avoids rerunning the whole Streamlit app every 2 sec.
    # The expensive Ollama translation is on a separate single worker thread.
    @st.fragment(run_every='2s')
    def _progress():
        reload_locale_cache()
        done, total = locale_coverage(lang)
        if done == total:
            st.rerun()
        st.progress(done / max(total, 1), text=message(lang, 'progress').format(done=done, total=total))
        state = job_status(lang)
        if state in ('failed', 'incomplete'):
            st.warning(message(lang, 'error'))
            if st.button(message(lang, 'retry'), key='retry_pack_' + lang):
                retry_job(lang)
                st.rerun()
    _progress()
