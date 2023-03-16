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

st.set_page_config(
    page_title= "Jurnatama",
    page_icon="OOO"
)

with open('custom.css') as source_des:
    st.markdown("<style>{source_des.read()}</style>", unsafe_allow_html=True)

CSS_LINKS = """<link href="assets/img/favicon.png" rel="icon">
<link href="assets/img/apple-touch-icon.png" rel="apple-touch-icon">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,600;1,700&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">
<link href="assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
<link href="assets/vendor/bootstrap-icons/bootstrap-icons.css" rel="stylesheet">
<link href="assets/vendor/fontawesome-free/css/all.min.css" rel="stylesheet">
<link href="assets/vendor/glightbox/css/glightbox.min.css" rel="stylesheet">
<link href="assets/vendor/swiper/swiper-bundle.min.css" rel="stylesheet">
<link href="assets/vendor/aos/aos.css" rel="stylesheet">
<link href="assets/css/main.css" rel="stylesheet">
"""

CSS_TABLE_LISTS = """
<div class="col-lg-4" data-aos="fade-up" data-aos-delay="100">
            <div class="pricing-item">
              <h3>Free Plan</h3>
              <h4><sup>$</sup>0<span> / month</span></h4>
              <ul>
                <li><i class="bi bi-check"></i> Quam adipiscing vitae proin</li>
                <li><i class="bi bi-check"></i> Nec feugiat nisl pretium</li>
                <li><i class="bi bi-check"></i> Nulla at volutpat diam uteera</li>
                <li class="na"><i class="bi bi-x"></i> <span>Pharetra massa massa ultricies</span></li>
                <li class="na"><i class="bi bi-x"></i> <span>Massa ultricies mi quis hendrerit</span></li>
              </ul>
              <a href="#" class="buy-btn">Buy Now</a>
            </div>
          </div>"""

SEARCH_RESULT = """
<div>
<h4>{}</h4>
<h4>{}</h4>
<h4>{}</h4>
<h4>{}</h4>
<h4>{}</h4>
</div>
"""

# st.markdown(CSS_LINKS, unsafe_allow_html=True)

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
""", unsafe_allow_html=True)

def card(similarity, title, p_date):
    return f"""
        <div class="card">
          <h5 style="color:black;" class="card-header">Kemiripan: {similarity}%</h5>
          <div class="card-body">
            <h5 style="color:black;" class="card-title">{title}</h5>
            <p style="color:black;" class="card-text">{p_date}</p>
            <a style="color:white;" href="#" class="btn btn-primary">Go somewhere</a>
          </div>
        </div>
        <br>
    """

st.sidebar.success("Select a page above.")

df = pd.read_csv('JELIKU-1.csv')
df["Abstrak"].fillna("Abstrak tidak tersedia", inplace=True)

#judul to dict
# jud = df['Judul']
# jud = dict(jud)

#abstrak to dict
# abs = df['Abstrak']
# abs = abs.loc[1:79]
# abs_dict = abs.to_dict()

df = df.loc[1:79]
df1 = df.to_dict('index')
df2 = df.to_dict()
abs_dict = df2['Abstrak']

# st.write(abs_dict)
# st.write(df1)

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Input a text here", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    #add to dictionary
    abs_dict[80] = my_input

    #tf idf
    tf_idf = TfidfVectorizer(stop_words='english')
    inverted_index = tf_idf.fit_transform(abs_dict.values())
    text_tfidf_result = pd.DataFrame(inverted_index.toarray(), index=abs_dict.keys(), columns=tf_idf.get_feature_names_out())

    #menyimpan hasil tf idf
    ttr = text_tfidf_result

    #mengambil indeks selain parameter
    col = ttr.columns.values
    row = ttr.index.values
    row = row[row != 80]

    #perhitungan cossim
    sum_d = []

    for a in row:
        temp = 0
        for b in col:
            ttr[b][a] = ttr[b][a] * ttr[b][80]
            temp = temp + ttr[b][a]
        sum_d.append(temp)

    # st.write(ttr)
    # st.write("=========================================================")
    # st.write(ttr_2)

    ttr_2 = pd.read_excel('text_tfidf_result_2.xlsx', index_col=0)

    #perhitungan cossim tahap 2 (kuadrat)
    col_2 = ttr_2.columns.values
    row_2 = ttr_2.index.values

    sum_d_kuadrat = []

    for a in row_2:
        temp = 0
        for b in col_2:
            ttr_2[b][a] = ttr_2[b][a] * ttr_2[b][a]
            temp = temp + ttr_2[b][a]
        sum_d_kuadrat.append(temp)

    #perhitungan cossim tahap 3 (akar kuadrat)
    sum_d_akar_kuadrat = []

    for a in sum_d_kuadrat:
        akar = math.sqrt(a)
        sum_d_akar_kuadrat.append(akar)

    #perhitungan cossim tahap 4 (terakhir)
    cossim_result = []

    for sum in range(79):
        temp = sum_d_akar_kuadrat[sum] * sum_d_akar_kuadrat[3]
        temp1 = sum_d[sum] / temp
        temp1 = round((temp1 * 100), 2)

        cossim_result.append(temp1)

    #replace hasil ke dictionary lengkap
    temp2 = 1
    for cossim in cossim_result:
        df1[temp2]['similarity'] = cossim
        temp2+=1

    # st.write(df1)
    #sorting dari nilai kemiripan tertinggi
    res = sorted(df1.items(), key=lambda x: x[1]['similarity'], reverse=True)

    st.write("Hasil perhitungan Cosine Similarity: ")

    # st.write(res)
    for r in res:
        # st.markdown(CSS_TABLE_LISTS, unsafe_allow_html=True)
        title = r[1]['Judul']
        abstract = r[1]['Abstrak']
        p_date = r[1]['Tanggal']
        author = r[1]['Author']
        journal = r[1]['Jurnal']
        similarity = r[1]['similarity']
        st.markdown(card(similarity, title, p_date), unsafe_allow_html=True)


