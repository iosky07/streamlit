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

import time

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

with st.form('crawling form'):
    choice = st.text_input('Masukkan Link Jurnal Garuda', st.session_state["my_input"])
    submit = st.form_submit_button('Submit')

if submit:
    progress_text = "Proses Crawling data. Mohon Tunggu."
    progress_text_2 = "Selesai."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.progress(percent_complete + 1, text=progress_text_2)

    st.success('Crawling data telah berhasil!', icon="✅")

    df1 = pd.read_excel('datasets/testing journals.xlsx', index_col=0)

    buffer = io.BytesIO()

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write each dataframe to a different worksheet.
        df1.to_excel(writer, sheet_name='Sheet1')

        # Close the Pandas Excel writer and output the Excel file to the buffer
        writer.save()

        st.download_button(
            label="Download Excel worksheets",
            data=buffer,
            file_name="download_test.xlsx",
            mime="application/vnd.ms-excel"
        )