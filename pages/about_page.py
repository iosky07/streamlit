import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import io

st.set_page_config(
    page_title="Simi",
    page_icon="🧊",
)

selected = option_menu("Main Menu", ['Home', 'Crawling', 'About'], icons=['house', 'list-columns-reverse', 'person'], menu_icon='cast', default_index=2, orientation='horizontal')

# st.markdown(CSS_LINKS, unsafe_allow_html=True)

if selected == 'Crawling':
    switch_page('crawling page')
elif selected == 'Home':
    switch_page('main')

st.write()

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
.med-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Simi</p>', unsafe_allow_html=True)
st.markdown('<p class="med-font; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>', unsafe_allow_html=True)
