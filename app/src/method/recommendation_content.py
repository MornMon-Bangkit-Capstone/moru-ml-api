import pandas as pd
import numpy as np
import pickle5 as pickle
import string
import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from sklearn.metrics.pairwise import cosine_similarity

eng = stopwords.words('english')

list_stopwords = eng

def load_data():
    # Load data
    with open('./data/cek1V2.pkl', 'rb') as f:
        df = pickle.load(f)
    return df

def recommendation_by_keyword(judul, jumlah):
    data_buku = load_data()
    data_buku['soup'] = data_buku['soup'].agg(lambda x: ' '.join(map(str, x)))

    judul = judul.lower()
    judul = pd.Series(judul)
    judul = judul.apply(lambda x: re.sub(r"\d+", "", x))
    judul = judul.apply(lambda x: x.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+—"}))
    judul = judul.apply(lambda x: x.strip())
    judul = judul.apply(lambda x: re.sub('\s+',' ', x))
    judul = judul.apply(lambda x: re.sub(r"\b[a-zA-Z]\b", "", x))

    judul = judul.apply(lambda x: word_tokenize(x))

    # Ambil kata kunci
    judul = judul.to_string()
    judul = judul[6:-1]
    judul = re.sub(r'[^\w\s]', '', judul)
    # Membaca data
    books = data_buku
    gnr = judul
    data = [{'Book-Title': judul, 'Book-Author': judul, 'Genres': gnr, 'Summary': judul ,  'book_title_list': judul, 'book_author_list': judul, 'genres_list': judul, 'summary_list': judul , 'soup': judul}]
    # books.drop_duplicates(subset ="title", inplace = True)
    # Menggabungkan database buku dengan kata kunci yang dimasukkan
    print(data)
    new = pd.DataFrame(data)
    frames = [books, new]
    # print(frames)
    result = pd.concat(frames)

    books = result.copy()
    # print(books)
    tfidf = TfidfVectorizer(stop_words=list_stopwords)
    tfidf_matrix = tfidf.fit_transform(books['soup'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    books = books.reset_index()
    titles = books['Book-Title']
    # print(titles)
    # titles = titles.str.lower()
    # summarry = books['Summary']
    # summarry = summarry.str.lower()
    authors = books['Book-Author']
    # Implementasi kode pada Gambar 4.7 (tanpa set genre menjadi lowercase)
    books['Genres'] = books['Genres'].apply(lambda x:x.replace("'", "").replace("[", "").replace("]", ""))
    books['Genres'] = [', '.join(map(str, l)) for l in books['Genres']]
    genres = books['Genres']
    indices = pd.Series(books.index, index=titles)
    # Memebentuk tampilan dataframe berdasarkan judul, penulis, genre dan cover
    jumlah = int(jumlah) + 1
    rec = []
    count = 0
    idx = indices[judul]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:jumlah]
    book_indices = [i[0] for i in sim_scores]
    for i in book_indices:
        Judul = titles.iloc[book_indices[count]]
        Penulis = authors.iloc[book_indices[count]]
        Genre = genres.iloc[book_indices[count]]
        Score = sim_scores[count][1]
        rec.append({'Judul': Judul, 'Penulis': Penulis})
        count += 1
    # rec = rec.sort_values(by='Score', ascending=False).head(jumlah)
    return rec


