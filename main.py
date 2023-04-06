import io
import itertools

import streamlit as st
import plotly.express as px
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

st.set_page_config(
    page_title= "Jurnatama",
    page_icon="OOO"
)

# st.markdown(CSS_LINKS, unsafe_allow_html=True)

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
""", unsafe_allow_html=True)

def card(similarity, title, p_date, download_link, number):
    return f"""
        <div class="card">
          <h5 style="color:black;" class="card-header">Kemiripan: {similarity}%</h5>
          <p style="color:black;" class="card-header">{number}</p>
          <div class="card-body">
            <h5 style="color:black;" class="card-title">{title}</h5>
            <p style="color:black;" class="card-text">{p_date}</p>
            <a style="color:white;" href="{download_link}" class="btn btn-primary">Download</a>
          </div>
        </div>
        <br>
    """

# st.sidebar.success("Select a page above.")

# df = pd.read_csv('JELIKU-1.csv')
df = pd.read_excel('datasets/testing journals.xlsx', index_col=0)
df["Abstrak"].fillna("Abstrak tidak tersedia", inplace=True)

#judul to dict
# jud = df['Judul']
# jud = dict(jud)

#abstrak to dict
# abs = df['Abstrak']
# abs = abs.loc[1:79]
# abs_dict = abs.to_dict()

df1 = df.to_dict('index')
df2 = df.to_dict()
abs_dict = df2['Abstrak']

# st.write(abs_dict)
# st.write(df)

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Input a text here", st.session_state["my_input"])
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
    # st.write("Tahap 1")
    # nltk.download('punkt')
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
                # print(token)
                tokens.remove(token)
                break

    # convert to string text
    abs_result = ' '.join(tokens)

    # duplikasi ke dataframe
    main_text_result = abs_result

    #add to dictionary
    # st.write("abs_dict type = {}".format(type(abs_dict)))
    # st.write("len abs_dict = {}".format(len(abs_dict)))
    abs_dict[501] = main_text_result
    # st.write("len abs_dict now = {}".format(len(abs_dict)))
    # st.write("len(df2)+1 = {}".format(len(df2)+1))

    #tf idf
    # st.write("Tahap 2")
    tf_idf = TfidfVectorizer(stop_words='english')
    inverted_index = tf_idf.fit_transform(abs_dict.values())
    # inverted_index_result = tf_idf.fit_transform(abs_dict[501])
    ttr = pd.DataFrame(inverted_index.toarray(), index=abs_dict.keys(), columns=tf_idf.get_feature_names_out())
    ttr_2 = pd.DataFrame(inverted_index.toarray(), index=abs_dict.keys(), columns=tf_idf.get_feature_names_out())

    # st.write("cek")
    # with io.BytesIO() as buffer:
    #     # Write array to buffer
    #     np.savetxt(buffer, ttr, delimiter=",")
    #     st.download_button(
    #         label="Download array as CSV",
    #         data=buffer,  # Download buffer
    #         file_name='array.csv',
    #         mime='text/csv'
    #     )

    # st.write("BENTUK DF {}" .format(ttr))
    # st.write("BENTUK DF Result {}" .format(ttr.iloc[[140]]))

    #menyimpan hasil tf idf
    # ttr = text_tfidf_result

    # col1 = ttr.columns
    # row1 = ttr.index
    # st.write("C1 {}".format(col1))
    # st.write("R1 {}".format(row1))

    #mengambil indeks selain parameter
    # col = ttr.columns.values
    # row = ttr.index.values
    # row = row[row != 501]
    # st.write("Tipe data col {}" .format(type(col)))
    # st.write("Tipe data row {}".format(type(row)))
    #
    # st.write("BENTUK COL {}" .format(col))
    # st.write("BENTUK ROW {}" .format(row))

    #perhitungan cossim
    # st.write("Tahap 3")
    # st.write("C {}" .format(col))
    # st.write("R {}".format(row))
    # sum_d = []

    #PENTING!!!
    temp = ttr.iloc[0: 499]
    temp = temp.to_numpy()
    tempp = ttr.loc[[501]]
    tempp = tempp.to_numpy()
    temp = ttr * tempp
    sum_d = temp.sum(axis=1)
    # st.write("SUM D {}".format(sum_d))

    # for a in row:
    #     temp = 0
    #     st.write("ROW {}" .format(a))
        # for b in col:
        #     st.write("COL {}".format(b))
        #     ttr[b][a] = ttr[b][a] * ttr[b][501]
        #     temp = temp + ttr[b][a]
        # sum_d.append(temp)

    # st.write(ttr)
    # st.write("=========================================================")
    # st.write(ttr_2)

    # ttr_2 = pd.read_excel('text_tfidf_result_2.xlsx', index_col=0)

    # st.write("BERHASILLLLLLL")
    #perhitungan cossim tahap 2 (kuadrat)
    # col_2 = ttr_2.columns.values
    # row_2 = ttr_2.index.values

    # sum_d_kuadrat = []

    temp_2 = ttr_2 * ttr_2
    sum_d_kuadrat = temp_2.sum(axis=1)
    # for a in row_2:
    #     temp = 0
    #     for b in col_2:
    #         ttr_2[b][a] = ttr_2[b][a] * ttr_2[b][a]
    #         temp = temp + ttr_2[b][a]
    #     sum_d_kuadrat.append(temp)

    # st.write("BERHASILLLLLLL 22222222222")

    #perhitungan cossim tahap 3 (akar kuadrat)
    sum_d_akar_kuadrat = []

    for a in sum_d_kuadrat:
        akar = math.sqrt(a)
        sum_d_akar_kuadrat.append(akar)

    # st.write("KUADRRAT {}" .format(sum_d_kuadrat))
    # st.write("AKAR KUADRRAT {}" .format(sum_d_akar_kuadrat))
    #perhitungan cossim tahap 4 (terakhir)
    # st.write("Tahap 4")
    cossim_result = []

    for sum in range(500):
        temp = sum_d_akar_kuadrat[sum] * sum_d_akar_kuadrat[3]
        temp1 = sum_d[sum] / temp
        temp1 = round((temp1 * 100), 2)
        cossim_result.append(temp1)

    #replace hasil ke dictionary lengkap
    temp2 = 0
    df_rep = dict(itertools.islice(df1.items(), 500))
    # st.write(cossim_result)
    for cossim in cossim_result:
        # st.write(cossim)
        df_rep[temp2]['similarity'] = cossim
        temp2+=1

    # st.write(len(cossim_result))
    # st.write(df_rep)
    #sorting dari nilai kemiripan tertinggi
    res = sorted(df_rep.items(), key=lambda x: x[1]['similarity'], reverse=True)
    res = res[:100]
    # st.write(res)

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
    # ti = type(df1)

    # st.write("Total Artikel Teknologi Informasi : {}" .format(ti))
    # st.write("Total Artikel Ilmu Geografi       : {}" .format(ig))
    # st.write("Total Artikel Ilmu Kimia          : {}" .format(ik))
    # st.write("Total Artikel Ilmu Hukum          : {}" .format(ih))
    # st.write("Total Artikel Kesehatan Masyarakat: {}" .format(km))

    st.write("Hasil perhitungan Cosine Similarity: ")


    # st.write(res)
    number = 0
    for r in res:
        # st.markdown(CSS_TABLE_LISTS, unsafe_allow_html=True)
        number += 1
        title = r[1]['Judul']
        abstract = r[1]['Abstrak']
        p_date = r[1]['Tanggal']
        author = r[1]['Author']
        journal = r[1]['Jurnal']
        download_link = r[1]['Link Download']
        similarity = r[1]['similarity']
        st.markdown(card(similarity, title, p_date, download_link, number), unsafe_allow_html=True)


