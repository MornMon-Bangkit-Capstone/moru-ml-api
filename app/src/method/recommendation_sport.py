import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import pickle5 as pickle

def load_data():
    with open('./data/data_sports.pkl', 'rb') as f:
        data_sport = pickle.load(f)
    with open('./data/cosine_sim_df_sport.pkl', 'rb') as f:
        cosine_sim_df = pickle.load(f)
    return data_sport, cosine_sim_df


def sports_recommendations(Sports, k=10):
    items, similarity_data = load_data() 
    items = items[['Sports', 'Muscle','Duration (Min)','Category']]
    index = similarity_data.loc[:,Sports].to_numpy().argpartition(range(-1, -k, -1))
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    closest = closest.drop(Sports, errors='ignore')
    
    recommendations = pd.DataFrame(closest).merge(items)
    
    similarity_values = [similarity_data.loc[Sports, sport] for sport in closest]
    recommendations['Similarity'] = similarity_values
    recommendations = recommendations.head(k)
    recom_list = recommendations['Sports'].tolist()
    return recom_list