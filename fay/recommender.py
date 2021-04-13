# /usr/bin/env python
import pandas as pd
import numpy as np
import random
import os
#import pickle
import re

from mysql.connector import MySQLConnection
import pymysql
from sqlalchemy import create_engine
import emoji

from sklearn.decomposition import NMF

# Connection to the server (MySQL)
USER=${FAY_MYSQL_USER}
HOST=${FAY_MYSQL_HOST}
PASSWORD=${FAY_MYSQL_PASSWORD}
PORT='3306'
DB=${FAY_MYSQL_DB}
engine = create_engine('mysql+pymysql://'+USER+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+DB)

fadb = pd.read_sql_query("SELECT * FROM fadb_cases", engine)
fadb['tags'] = fadb['tags'].replace('[?⚡⚽⚫✈️]', ',', regex = True) # Remove question marks which replcaed the emojis
fadb['tags'] = fadb['tags'].replace('[\U00010000-\U0010ffff]', ',', regex = True) # Remove all emojis
fadb['tags'] = fadb['tags'].replace(',,', ',', regex = True) # Remove double commas with single comma
fadb['tags'] = fadb['tags'].replace('\s*,\s*',', ', regex = True) # Remove the spacings before and after commas
fadb['tags'] = fadb['tags'].replace('(^..)','', regex = True) # !! This one should be replaced by a better regex or a for-loop to remove leading comma in a string
fadb['tags'] = fadb['tags'].replace('^\s+', '', regex = True) # Remove white space at the beginning of the string
fadb['tags'] = fadb['tags'].replace('[ \t]+$','', regex = True) # Remove white space at the end of the string
fadb['url'] = fadb['url'].replace('\?utm_source.+','', regex = True) # Remove the tracking link ?utm_source=Future+Atelier...
fadb['url'] = fadb['url'].replace('utm_source.+','', regex = True)

fadb_url = fadb.set_index('url')

df = fadb_url[['tags']]
x = df.tags.str.split('\s*,\s*', expand=True).stack()
df = pd.crosstab(x.index.get_level_values(0), x.values).iloc[:, 1:]
df = df.reset_index()

clicks = pd.read_sql_query("SELECT * FROM fadb_newsletter_clicks", engine)
clicks = clicks.drop(columns=['id','campaign','First Name','Last Name','Address','Phone Number','Birthday','Opt-in','LinkedIn','Member Rating'])
clicks['URL'] = clicks['URL'].replace('\?utm_source.+','', regex = True) # Remove the tracking link ?utm_source=Future+Atelier...
clicks['URL'] = clicks['URL'].replace('utm_source.+','', regex = True)
clicks = clicks.rename(columns={"URL": "url"})

joined_df = pd.concat([df, clicks], axis=1, join="inner")

joined_df_tag = pd.concat([df, clicks], axis=1, join="inner")
joined_df_tag.name = 'joined_df_tag'
joined_df_tag = joined_df_tag.groupby(['Email Address']).sum()
joined_df_tag = joined_df_tag.drop(columns=['Clicks'])
#pd.DataFrame(joined_df_tag.T.reset_index()["index"]).to_csv("tag_dict.csv")

joined_df_url = pd.concat([df, clicks], axis=1, join="inner")
joined_df_tag.name = 'joined_df_url'
joined_df_url = pd.pivot_table(joined_df, values='Clicks', index=['Email Address'], columns=['url'], fill_value=0)

joined_df_tag_url = df
joined_df_tag_url = joined_df_tag_url.set_index("row_0")


def get_recommendation(user_input: dict):   

    print(user_input)
    
    t1 = user_input.get("i1", "Does not exist")

    t2 = user_input.get("i2", "Does not exist")

    t3 = user_input.get("i3", "Does not exist")

    joined_df = joined_df_tag
    #tag_dict = pd.read_csv("data/tag_dict.csv")
    tag_dict = pd.read_sql_query("SELECT * FROM tag_dict", engine)

    average_score = joined_df.mean().mean()
    max_score = joined_df.max().max()

    input_list = []
    query = [[average_score] * len(joined_df.T)]

    if t1 != "Does not exist":
        t1 = re.sub('[?⚡⚽⚫✈️]',',', t1)
        t1 = re.sub('[\U00010000-\U0010ffff]',',',t1)
        t1 = re.sub(',,', ',',t1)
        t1 = re.sub('\s*,\s*',', ',t1)
        t1 = re.sub('(^..)','',t1)
        t1 = re.sub('^\s+', '',t1)
        t1 = re.sub('[ \t]+$','',t1)

        t1 = re.sub('\,.*$','', t1)
        print("DEBUGGING", t1)
        t1 = tag_dict[tag_dict["tag"] == t1]["id"].tolist()[0]
        i1 = t1
        query[0][i1] = max_score
        input_list.append(t1)

    if t2 != "Does not exist":
        t2 = re.sub('[?⚡⚽⚫✈️]',',', t2)
        t2 = re.sub('[\U00010000-\U0010ffff]',',',t2)
        t2 = re.sub(',,', ',',t2)
        t2 = re.sub('\s*,\s*',', ',t2)
        t2 = re.sub('(^..)','',t2)
        t2 = re.sub('^\s+', '',t2)
        t2 = re.sub('[ \t]+$','',t2)

        t2 = re.sub('\,.*$','', t2)
        t2 = tag_dict[tag_dict["tag"] == t2]["id"].tolist()[0]
        i2 = t2
        query[0][i2] = max_score
        input_list.append(t2)

    if t3 != "Does not exist":
        t3 = re.sub('[?⚡⚽⚫✈️]',',', t3)
        t3 = re.sub('[\U00010000-\U0010ffff]',',',t3)
        t3 = re.sub(',,', ',',t3)
        t3 = re.sub('\s*,\s*',', ',t3)
        t3 = re.sub('(^..)','',t3)
        t3 = re.sub('^\s+', '',t3)
        t3 = re.sub('[ \t]+$','',t3)

        t3 = re.sub('\,.*$','', t3)
        t3 = tag_dict[tag_dict["tag"] == t3]["id"].tolist()[0]
        i3 = t3
        query[0][i3] = max_score
        input_list.append(t3)

    
    
    ### Fitting the mdoel
    
    R = joined_df.values
    model = NMF(n_components=8, init='random', random_state=10)
    model.fit(R) 




    Q = model.components_  # tag-genre matrix
    P = model.transform(R)  # user-genre matrix
    nR = np.dot(P, Q) # The reconstructed matrix!

    # Creating empty list for querys and rewriting these predict the hidden features for a new data point
    query_df = pd.DataFrame(query)
    profile = model.transform(query_df)
    tags_preds = np.dot(profile, Q).round(2)

    tags = list(joined_df.columns)
    tags[tags_preds.argmax()]

    predictions = tags[tags_preds.argmax()]
    top_preds = np.argsort(-tags_preds)
    top_predictions = pd.DataFrame(top_preds)
    recommendations = top_predictions.iloc[0][:10].to_dict()

    for i in range(len(recommendations)):
        if recommendations[i] in input_list:
            del recommendations[i]

    best_recommendation_1 = tags[recommendations[len(input_list)]]
    u1 = df[df[best_recommendation_1] == 1]['row_0'].tolist()[0]

    best_recommendation_2 = tags[recommendations[len(input_list)+1]]
    u2 = df[df[best_recommendation_2] == 1]['row_0'].tolist()[0]

    best_recommendation_3 = tags[recommendations[len(input_list)+2]]
    u3 = df[df[best_recommendation_3] == 1]['row_0'].tolist()[0]

    best_recommendation = (best_recommendation_1, best_recommendation_2, best_recommendation_3, u1, u2, u3)

    return best_recommendation

if __name__ == '__main__':
    """good place for test code """
    print('HELLO TENSORS!')
    predicted_food = get_recommendation()
    print(best_recommendation)