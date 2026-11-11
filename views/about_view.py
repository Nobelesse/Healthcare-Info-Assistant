"""Project-only About page: no college, academic or developer details."""
from html import escape
import streamlit as st
from ui.components import hero, section, feature_card, advisory
from ui.strings import t


def about_page(lang='en'):
    hero(language=lang,landing=True)
    st.write('')
    section(t('about_title',lang),t('about_desc',lang),t('about_overline',lang))
    st.markdown(t('about_intro',lang))
    cards=[('about_card_chat','about_card_chat_desc','🧠'),
           ('about_card_report','about_card_report_desc','📊'),
           ('about_card_voice','about_card_voice_desc','🎙')]
    for col,(title,desc,icon) in zip(st.columns(3),cards):
        with col: feature_card(t(title,lang),t(desc,lang),icon)
    st.write('')
    section(t('about_how',lang),t('about_how_desc',lang),t('about_how_overline',lang))
    tiles=''.join(f'<div class="system-tile">{icon} {escape(t(key,lang))}</div>' for key,icon in [
        ('about_step_1','🖥'),('about_step_2','🧠'),('about_step_3','🗣'),
        ('about_step_4','📄'),('about_step_5','🔐'),('about_step_6','🎤')])
    st.markdown(f'<div class="glass-panel system-steps">{tiles}</div>',unsafe_allow_html=True)
    section(t('about_privacy',lang),t('about_privacy_desc',lang),t('about_privacy_overline',lang))
    for i in range(1,7):
        st.markdown('• '+t(f'about_privacy_{i}',lang))
    st.markdown('#### '+t('about_resources',lang))
    st.markdown('[WHO](https://www.who.int/health-topics) · [MedlinePlus](https://medlineplus.gov/) · '
                '[NHS](https://www.nhs.uk/conditions/) · '
                '[NIH](https://ods.od.nih.gov/)')
    advisory(lang)
