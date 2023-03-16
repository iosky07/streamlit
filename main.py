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

st.title("Pencarian Artikel")
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

    st.write(res)

