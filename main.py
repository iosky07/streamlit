import io
import itertools

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math
from itertools import zip_longest
from collections import OrderedDict
from operator import getitem
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Simi",
    page_icon="🧊",
)

# selected = 'Home'
selected = option_menu("Main Menu", ['Home', 'Crawling', 'About'], icons=['house', 'list-columns-reverse', 'person'], menu_icon='cast', default_index=0, orientation='horizontal')

# st.markdown(CSS_LINKS, unsafe_allow_html=True)

if selected == 'Crawling':
    switch_page('crawling page')
elif selected == 'About':
    switch_page('about page')

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
""", unsafe_allow_html=True)
def card(similarity, title, p_date, download_link, number):
    return f"""
        <div class="card">
          <h5 style="color:black;" class="card-header">Kemiripan: {similarity}%</h5>
          <h5 style="color:black;" class="card-header">{title}</h5>
          <div class="card-body">
            <p style="color:black;" class="card-text">{abstract[0:300]}....</p>
            <a style="color:white;" href="{download_link}" class="btn btn-primary">Download</a>
          </div>
        </div>
        <br>
    """

# st.sidebar.success("Select a page above.")

df = pd.read_excel('datasets/testing journals.xlsx', index_col=0)
df["Abstrak"].fillna("Abstrak tidak tersedia", inplace=True)

df1 = df.to_dict('index')
df2 = df.to_dict()
abs_dict = df2['Abstrak']

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Masukkan teks abstrak", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    #PREPROCESSING TEKS INPUTAN
    hasil = my_input
    hasil2 = my_input

    # lowercase
    hasil.lower()
    hasil2.lower()

    # create stemmer
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stem = stemmer.stem(hasil)
    stem2 = stemmer.stem(hasil2)

    # tokenizing
    tokens = nltk.tokenize.word_tokenize(stem)
    temp_tokens = nltk.tokenize.word_tokenize(stem2)

    # menghilangkan duplikasi
    tokens = list(dict.fromkeys(tokens))
    temp_tokens = list(dict.fromkeys(temp_tokens))

    #list stopword
    stopwords = ['ada', 'adanya', 'adalah', 'adapun', 'agak', 'agaknya', 'agar', 'akan', 'akankah', 'akhirnya', 'aku',
                 'akulah', 'amat', 'amatlah', 'anda', 'andalah', 'antar', 'diantaranya', 'antara', 'antaranya',
                 'diantara', 'apa', 'apaan', 'mengapa', 'apabila', 'apakah', 'apalagi', 'apatah', 'atau', 'ataukah',
                 'ataupun', 'bagai', 'bagaikan', 'sebagai', 'sebagainya', 'bagaimana', 'bagaimanapun', 'sebagaimana',
                 'bagaimanakah', 'bagi', 'bahkan', 'bahwa', 'bahwasanya', 'sebaliknya', 'banyak', 'sebanyak',
                 'beberapa', 'seberapa', 'begini', 'beginian', 'beginikah', 'beginilah', 'sebegini', 'begitu',
                 'begitukah', 'begitulah', 'begitupun', 'sebegitu', 'belum', 'belumlah', 'sebelum', 'sebelumnya',
                 'sebenarnya', 'berapa', 'berapakah', 'berapalah', 'berapapun', 'betulkah', 'sebetulnya', 'biasa',
                 'biasanya', 'bila', 'bilakah', 'bisa', 'bisakah', 'sebisanya', 'boleh', 'bolehkah', 'bolehlah', 'buat',
                 'bukan', 'bukankah', 'bukanlah', 'bukannya', 'cuma', 'percuma', 'dahulu', 'dalam', 'dan', 'dapat',
                 'dari', 'daripada', 'dekat', 'demi', 'demikian', 'demikianlah', 'sedemikian', 'dengan', 'depan', 'di',
                 'dia', 'dialah', 'dini', 'diri', 'dirinya', 'terdiri', 'dong', 'dulu', 'enggak', 'enggaknya', 'entah',
                 'entahlah', 'terhadap', 'terhadapnya', 'hal', 'hampir', 'hanya', 'hanyalah', 'harus', 'haruslah',
                 'harusnya', 'seharusnya', 'hendak', 'hendaklah', 'hendaknya', 'hingga', 'sehingga', 'ia', 'ialah',
                 'ibarat', 'ingin', 'inginkah', 'inginkan', 'ini', 'inikah', 'inilah', 'itu', 'itukah', 'itulah',
                 'jangan', 'jangankan', 'janganlah', 'jika', 'jikalau', 'juga', 'justru', 'kala', 'kalau', 'kalaulah',
                 'kalaupun', 'kalian', 'kami', 'kamilah', 'kamu', 'kamulah', 'kan', 'kapan', 'kapankah', 'kapanpun',
                 'dikarenakan', 'karena', 'karenanya', 'ke', 'kecil', 'kemudian', 'kenapa', 'kepada', 'kepadanya',
                 'ketika', 'seketika', 'khususnya', 'kini', 'kinilah', 'kiranya', 'sekiranya', 'kita', 'kitalah', 'kok',
                 'lagi', 'lagian', 'selagi', 'lah', 'lain', 'lainnya', 'melainkan', 'selaku', 'lalu', 'melalui',
                 'terlalu', 'lama', 'lamanya', 'selama', 'selama', 'selamanya', 'lebih', 'terlebih', 'bermacam',
                 'macam', 'semacam', 'maka', 'makanya', 'makin', 'malah', 'malahan', 'mampu', 'mampukah', 'mana',
                 'manakala', 'manalagi', 'masih', 'masihkah', 'semasih', 'masing', 'mau', 'maupun', 'semaunya',
                 'memang', 'mereka', 'merekalah', 'meski', 'meskipun', 'semula', 'mungkin', 'mungkinkah', 'nah',
                 'namun', 'nanti', 'nantinya', 'nyaris', 'oleh', 'olehnya', 'seorang', 'seseorang', 'pada', 'padanya',
                 'padahal', 'paling', 'sepanjang', 'pantas', 'sepantasnya', 'sepantasnyalah', 'para', 'pasti',
                 'pastilah', 'per', 'pernah', 'pula', 'pun', 'merupakan', 'rupanya', 'serupa', 'saat', 'saatnya',
                 'sesaat', 'saja', 'sajalah', 'saling', 'bersama', 'sama', 'sesama', 'sambil', 'sampai', 'sana',
                 'sangat', 'sangatlah', 'saya', 'sayalah', 'se', 'sebab', 'sebabnya', 'sebuah', 'tersebut',
                 'tersebutlah', 'sedang', 'sedangkan', 'sedikit', 'sedikitnya', 'segala', 'segalanya', 'segera',
                 'sesegera', 'sejak', 'sejenak', 'sekali', 'sekalian', 'sekalipun', 'sesekali', 'sekaligus', 'sekarang',
                 'sekarang', 'sekitar', 'sekitarnya', 'sela', 'selain', 'selalu', 'seluruh', 'seluruhnya', 'semakin',
                 'sementara', 'sempat', 'semua', 'semuanya', 'sendiri', 'sendirinya', 'seolah', 'seperti', 'sepertinya',
                 'sering', 'seringnya', 'serta', 'siapa', 'siapakah', 'siapapun', 'disini', 'disinilah', 'sini',
                 'sinilah', 'sesuatu', 'sesuatunya', 'suatu', 'sesudah', 'sesudahnya', 'sudah', 'sudahkah', 'sudahlah',
                 'supaya', 'tadi', 'tadinya', 'tak', 'tanpa', 'setelah', 'telah', 'tentang', 'tentu', 'tentulah',
                 'tentunya', 'tertentu', 'seterusnya', 'tapi', 'tetapi', 'setiap', 'tiap', 'setidaknya', 'tidak',
                 'tidakkah', 'tidaklah', 'toh', 'untuk', 'waduh', 'wah', 'wahai', 'sewaktu', 'walau', 'walaupun',
                 'wong', 'yaitu', 'yakni', 'yang']

    # filtering/menghilangkan kata tak penting
    for token in temp_tokens:
        for stopword in stopwords:
            if token == stopword:
                tokens.remove(token)
                break

    # convert to string text
    abs_result = ' '.join(tokens)

    # duplikasi ke dataframe
    main_text_result = abs_result

    #add to dictionary
    abs_dict[501] = main_text_result

    #tf idf
    tf_idf = TfidfVectorizer(stop_words='english')
    inverted_index = tf_idf.fit_transform(abs_dict.values())
    ttr = pd.DataFrame(inverted_index.toarray(), index=abs_dict.keys(), columns=tf_idf.get_feature_names_out())
    ttr_2 = pd.DataFrame(inverted_index.toarray(), index=abs_dict.keys(), columns=tf_idf.get_feature_names_out())

    #perhitungan cossim
    #PENTING!!!
    temp = ttr.iloc[0: 499]
    temp = temp.to_numpy()
    tempp = ttr.loc[[501]]
    tempp = tempp.to_numpy()
    temp = ttr * tempp
    sum_d = temp.sum(axis=1)

    # perhitungan cossim tahap 2 (kuadrat)
    temp_2 = ttr_2 * ttr_2
    sum_d_kuadrat = temp_2.sum(axis=1)

    #perhitungan cossim tahap 3 (akar kuadrat)
    sum_d_akar_kuadrat = []

    for a in sum_d_kuadrat:
        akar = math.sqrt(a)
        sum_d_akar_kuadrat.append(akar)

    cossim_result = []

    for sum in range(500):
        temp = sum_d_akar_kuadrat[sum] * sum_d_akar_kuadrat[3]
        temp1 = sum_d[sum] / temp
        temp1 = round((temp1 * 100), 2)
        cossim_result.append(temp1)

    #replace hasil ke dictionary lengkap
    temp2 = 0
    df_rep = dict(itertools.islice(df1.items(), 500))
    for cossim in cossim_result:
        df_rep[temp2]['similarity'] = cossim
        temp2+=1

    res = sorted(df_rep.items(), key=lambda x: x[1]['similarity'], reverse=True)
    res = list(filter(lambda c: c[1]['similarity'] > 5, res))

    #menghitung frekuensi munculnya jenis artikel ilmiah
    ti = 0
    ig = 0
    ik = 0
    ih = 0
    km = 0

    for d in res:
        d_temp = d[1]['Tipe']
        if d_temp == "Teknologi Informasi":
            ti += 1
        elif d_temp == "Ilmu Geografi":
            ig += 1
        elif d_temp == "Ilmu Kimia":
            ik += 1
        elif d_temp == "Ilmu Hukum":
            ih += 1
        else:
            km += 1

    #Perhitungan nilai uji
    act_doc = 100
    # st.write(res[0][1]["Tipe"])

    if res[0][1]["Tipe"] == "Ilmu Hukum":
        prec = ih / (ih + (ig + ik + ti + km))
        rec = ih / act_doc
        f1 = (2 * prec * rec) / (prec + rec)

    elif res[0][1]["Tipe"] == "Teknologi Informasi":
        prec = ti / (ti + (ig + ik + ih + km))
        rec = ti / act_doc
        f1 = (2 * prec * rec) / (prec + rec)

    elif res[0][1]["Tipe"] == "Ilmu Kimia":
        prec = ik / (ik + (ig + km + ih + ti))
        rec = ik / act_doc
        f1 = (2 * prec * rec) / (prec + rec)

    elif res[0][1]["Tipe"] == "Ilmu Geografi":
        prec = ig / (ig + (km + ik + ih + ti))
        rec = ig / act_doc
        f1 = (2 * prec * rec) / (prec + rec)

    else:
        prec = km / (km + (ig + ik + ih + ti))
        rec = km / act_doc
        f1 = (2 * prec * rec) / (prec + rec)

    prec = round(prec * 100, 2)
    rec = round(rec * 100, 2)
    f1 = round(f1 * 100, 2)
    st.write("Precision {}%, Recall {}%, dan F1 Score {}%" .format(prec, rec, f1))

    # st.write("Total Artikel Teknologi Informasi : {}" .format(ti))
    # st.write("Total Artikel Ilmu Geografi       : {}" .format(ig))
    # st.write("Total Artikel Ilmu Kimia          : {}" .format(ik))
    # st.write("Total Artikel Ilmu Hukum          : {}" .format(ih))
    # st.write("Total Artikel Kesehatan Masyarakat: {}" .format(km))
    st.write("Hasil perhitungan Cosine Similarity: ")

    number = 0
    for r in res:
        number += 1
        title = r[1]['Judul']
        abstract = r[1]['Abstrak']
        p_date = r[1]['Tanggal']
        author = r[1]['Author']
        journal = r[1]['Jurnal']
        download_link = r[1]['Link Download']
        similarity = r[1]['similarity']
        st.markdown(card(similarity, title, p_date, download_link, number), unsafe_allow_html=True)


