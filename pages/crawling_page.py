import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import time
import bs4
import urllib.request as url
import pandas as pd
import io
from itertools import repeat
import numpy

st.set_page_config(
    page_title="Simi",
    page_icon="🧊",
)

selected = option_menu("Main Menu", ['Home', 'Crawling', 'About'], icons=['house', 'list-columns-reverse', 'person'], menu_icon='cast', default_index=1, orientation='horizontal')

# st.markdown(CSS_LINKS, unsafe_allow_html=True)

if selected == 'About':
    switch_page('about page')
elif selected == 'Home':
    switch_page('main')

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

def crawling(journal_link):
    my_bar = st.progress(0, text=progress_text)
    # confussion matrix
    response = url.urlopen(journal_link)
    # st.exception(response)

    page = bs4.BeautifulSoup(response)

    temp_page = 2
    i = "just temp"

    t_list = []
    au_list = []
    a_list = []
    jn_list = []
    d_list = []
    dl_list = []

    # supaya variabel journal bisa iterable
    journal = page.find('div', class_='j-meta-title')
    journal = journal.text.strip()

    while i != None:

        time.sleep(0.1)
        i = None
        # mengambil title
        titles = page.find_all('a', class_='title-article')
        for a in titles:
            a = a.text.strip()
            t_list.append(a)

        titles = t_list

        # mengambil nama author
        for j in page.find_all('div', class_='article-item'):
            temp_list = []
            for k in j.find_all('a', class_='author-article'):
                temp = k.text.strip()
                temp_list.append(temp)
            joined = " ,".join(temp_list)
            au_list.append(joined)

        # mengambil abstrak
        abstracts = page.find_all('xmp', class_='abstract-article')

        for a in abstracts:
            if a != None:
                a = a.text.strip()
                a_list.append(a)
            else:
                a = 'abstrak tidak tersedia'
                a_list.append(a)

        # mengambil nama jurnal (looping manipulasi)
        journal_names = page.find_all('xmp', class_='subtitle-article')
        for a in journal_names:
            jn_list.append(journal)

        # mengambil tanggal
        for a in page.find_all('a', class_='title-article', href=True):
            # print(a['href'])
            response2 = url.urlopen('https://garuda.kemdikbud.go.id{}'.format(a['href']))
            page2 = bs4.BeautifulSoup(response2)

            dates = page2.find_all('p')
            dates = dates[0].text.strip()
            d_list.append(dates)

        # mengambil link download
        temp = 1

        for i in page.find_all('a', class_='title-citation', href=True):
            if temp == 1:
                dl_list.append(i['href'])
                temp += 1
            elif temp == 2:
                temp += 1
            else:
                temp = 1
        # print(i)

        # set up crawling halaman selanjutnya
        response = url.urlopen('{}?page={}'.format(journal_link, temp_page))
        page = bs4.BeautifulSoup(response)
        # print(temp_page)
        # print(page)
        temp_page += 1
        my_bar.progress(temp_page + 1, text=progress_text)
    return [t_list, a_list, d_list, au_list, jn_list, dl_list, journal, my_bar];


choice = ['Crawling Semua Data', 'Crawling berdasarkan Link Jurnal']
result_c = st.radio('Pilih Jenis Crawling', choice)

if result_c == 'Crawling Semua Data':
    with st.form('crawling form'):
        choice_1 = st.selectbox('', ['Crawling Semua Data'], key=1, label_visibility='collapsed')
        submit = st.form_submit_button('Submit')

    if submit:
        # try:
            progress_text = "Proses Crawling data. Mohon Tunggu."
            progress_text_2 = "Selesai."

            j = "just temp"
            temp_web_page = 2

            response3 = url.urlopen('https://garuda.kemdikbud.go.id/journal/')
            page3 = bs4.BeautifulSoup(response3)

            t_list = []
            au_list = []
            a_list = []
            jn_list = []
            d_list = []
            dl_list = []

            while j != None:
                j = None

                tj_list = []

                for j in page3.find_all('a', class_='title-journal', href=True):
                    temp_tj = "https://garuda.kemdikbud.go.id{}".format(j['href'])
                    tj_list.append(temp_tj)

                if tj_list != []:
                    for k in tj_list:
                        def_list = crawling(k)
                        t_list = numpy.concatenate([t_list, def_list[0]])
                        a_list = numpy.concatenate([a_list, def_list[1]])
                        d_list = numpy.concatenate([d_list, def_list[2]])
                        au_list = numpy.concatenate((au_list, def_list[3]))
                        jn_list = numpy.concatenate([jn_list, def_list[4]])
                        dl_list = numpy.concatenate([dl_list, def_list[5]])
                        # journal = def_list[6]
                        my_bar = def_list[7]
                        st.write(au_list)

                    response3 = url.urlopen('https://garuda.kemdikbud.go.id/journal?page={}'.format(temp_web_page))
                    page3 = bs4.BeautifulSoup(response3)
                    # print(temp_page)
                    # print(page)
                    temp_web_page += 1

                else:
                    type_list = []
                    type_list.extend(repeat("Artikel Ilmiah", len(t_list)))

                    df = pd.DataFrame([*zip(t_list, a_list, d_list, au_list, jn_list, dl_list, type_list)])
                    df.columns = ['Judul', 'Abstrak', 'Tanggal', 'Author', 'Jurnal', 'Link Download', 'Tipe']

                    buffer = io.BytesIO()

                    # Create a Pandas Excel writer using XlsxWriter as the engine.
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        # Write each dataframe to a different worksheet.
                        df.to_excel(writer, sheet_name='Sheet1')

                        # Close the Pandas Excel writer and output the Excel file to the buffer
                        writer.save()
                        nama_file = "Data Crawling Jurnal Website Garuda.xlsx"
                        st.download_button(
                            label="Download Hasil Crawling",
                            data=buffer,
                            file_name=nama_file,
                            mime="application/vnd.ms-excel"
                        )

                    my_bar.progress(100, text=progress_text_2)
                    st.success('Crawling data telah berhasil!', icon="✅")

        # except:
        #     st.error('Mohon maaf, terjadi kesalahan dalam memuat halaman website tujuan', icon="🚨")

else:
    with st.form('crawling form'):
        # st.write(label)
        choice = st.text_input("Masukkan Link Jurnal Garuda (contoh kueri: https://garuda.kemdikbud.go.id/journal/view/1234)", st.session_state["my_input"])
        submit = st.form_submit_button('Submit')

    if submit:
        l_1 = 0
        l_2 = ""

        for i in choice:
            l_1 += 1
            if l_1 <= 44:
                l_2 = l_2 + i

        if l_2 == "https://garuda.kemdikbud.go.id/journal/view/":
            try:
                progress_text = "Proses Crawling data. Mohon Tunggu."
                progress_text_2 = "Selesai."

                #def
                def_list = crawling(choice)
                t_list = def_list[0]
                a_list = def_list[1]
                d_list = def_list[2]
                au_list = def_list[3]
                jn_list = def_list[4]
                dl_list = def_list[5]
                journal = def_list[6]
                my_bar = def_list[7]

                type_list = []
                type_list.extend(repeat("Artikel Ilmiah", len(t_list)))

                df = pd.DataFrame([*zip(t_list, a_list, d_list, au_list, jn_list, dl_list, type_list)])
                df.columns = ['Judul', 'Abstrak', 'Tanggal', 'Author', 'Jurnal', 'Link Download', 'Tipe']

                buffer = io.BytesIO()

                # Create a Pandas Excel writer using XlsxWriter as the engine.
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    # Write each dataframe to a different worksheet.
                    df.to_excel(writer, sheet_name='Sheet1')

                    # Close the Pandas Excel writer and output the Excel file to the buffer
                    writer.save()
                    nama_file = "Data Crawling {}.xlsx" .format(journal)
                    st.download_button(
                        label="Download Hasil Crawling",
                        data=buffer,
                        file_name=nama_file,
                        mime="application/vnd.ms-excel"
                    )

                my_bar.progress(100, text=progress_text_2)
                st.success('Crawling data telah berhasil!', icon="✅")
            except:
                st.error('Terjadi kesalahan dalam memuat halaman website tujuan (coba periksa data input)', icon="🚨")
        else:
            st.error('Data input kosong atau link yang anda masukkan salah', icon="🚨")


