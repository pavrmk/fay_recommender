from flask import Flask, render_template, make_response, jsonify, request
from fay.recommender import get_recommendation#, MOVIES

import pandas as pd
from mysql.connector import MySQLConnection
import pymysql
from sqlalchemy import create_engine
import emoji
import random


# Connection to the server (MySQL)
USER=${FAY_MYSQL_USER}
HOST=${FAY_MYSQL_HOST}
PASSWORD=${FAY_MYSQL_PASSWORD}
PORT='3306'
DB=${FAY_MYSQL_DB}
engine = create_engine('mysql+pymysql://'+USER+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+DB)

app = Flask(__name__)

@app.route('/recommender') # <-- decorator
def recommend():

    user_input = dict(request.args)
    ### THIS IS THE DATA THAT WAS ASSEMBLED BY THE FORM!
    user_input

    movie = get_recommendation(user_input)

    fadb_clean = pd.read_sql_query("SELECT * FROM fadb_cases", engine)

    recommended_tag_1 = get_recommendation(user_input)[0]
    u1 = get_recommendation(user_input)[3]
    i1 = fadb_clean[fadb_clean["url"] == u1]["image"].tolist()[0]
    h1 = fadb_clean[fadb_clean["url"] == u1]["title"].tolist()[0]
    p1 = fadb_clean[fadb_clean["url"] == u1]["summary"].tolist()[0]
    t1 = fadb_clean[fadb_clean["url"] == u1]["tags"].tolist()[0]

    recommended_tag_2 = get_recommendation(user_input)[1]
    u2 = get_recommendation(user_input)[4]
    i2 = fadb_clean[fadb_clean["url"] == u2]["image"].tolist()[0]
    h2 = fadb_clean[fadb_clean["url"] == u2]["title"].tolist()[0]
    p2 = fadb_clean[fadb_clean["url"] == u2]["summary"].tolist()[0]
    t2 = fadb_clean[fadb_clean["url"] == u2]["tags"].tolist()[0]

    recommended_tag_3 = get_recommendation(user_input)[3]
    u3 = get_recommendation(user_input)[5]
    i3 = fadb_clean[fadb_clean["url"] == u3]["image"].tolist()[0]
    h3 = fadb_clean[fadb_clean["url"] == u3]["title"].tolist()[0]
    p3 = fadb_clean[fadb_clean["url"] == u3]["summary"].tolist()[0]
    t3 = fadb_clean[fadb_clean["url"] == u3]["tags"].tolist()[0]

    fay_says = ["Hmm, I think I found something you might like", "Interesting choice!", "Let's see...", "Okay, here we go!", "Let's see what article suggestions I've discovered for you.", "Oh yes, you might like these results."]
    fay_says = random.choice(fay_says)

    return render_template('recommendation.html', fay_says=fay_says, recommended_tag_1=recommended_tag_1,recommended_tag_2=recommended_tag_2,recommended_tag_3=recommended_tag_3, u1=u1,i1=i1,h1=h1,p1=p1,t1=t1, u2=u2,i2=i2,h2=h2,p2=p2,t2=t2, u3=u3,i3=i3,h3=h3,p3=p3,t3=t3)

@app.route('/')
def main_page():

    df_to_choose_from = pd.read_sql_query("SELECT * FROM fadb_cases", engine)
    df_to_choose_from = df_to_choose_from[df_to_choose_from.image_caption != "1"]
    df_to_choose_from = df_to_choose_from[df_to_choose_from.image_caption != "2"]
    df_to_choose_from = df_to_choose_from[df_to_choose_from.image_caption != "3"]
    random_choice = df_to_choose_from.sample(3)

    i1 = random_choice["image"].iloc[0]
    h1 = random_choice["title"].iloc[0]
    p1 = random_choice["summary"].iloc[0]
    t1 = random_choice["tags"].iloc[0]
    u1 = random_choice["url"].iloc[0]

    i2 = random_choice["image"].iloc[1]
    h2 = random_choice["title"].iloc[1]
    p2 = random_choice["summary"].iloc[1]
    t2 = random_choice["tags"].iloc[1]
    u2 = random_choice["url"].iloc[1]

    i3 = random_choice["image"].iloc[2]
    h3 = random_choice["title"].iloc[2]
    p3 = random_choice["summary"].iloc[2]
    t3 = random_choice["tags"].iloc[2]
    u3 = random_choice["url"].iloc[2]

    return render_template('main_page.html', i1=i1, h1=h1, p1=p1, t1=t1, u1=u1, i2=i2, h2=h2, p2=p2, t2=t2, u2=u2, i3=i3, h3=h3, p3=p3, t3=t3, u3=u3)

#@app.route('/all')
#def all_movies():
#    data = {'movies' : MOVIES}
#    return make_response(jsonify(data))

#@app.route('/greet/<name>')
#def hello(name="human"): 
#    return "Hello " + name

#@app.route('/api/<movie1>&<movie2>&<movie3>')
#def simple_recommender(movie1, movie2, movie3):
#    data = {
#    'your_input': [movie1, movie2, movie3],
    # 'recommendation': nmf_recommender(movie1, movie2, movie3),
    # Ultimately what we want!!
    # i.e. a function that makes predictions BASED ON user input!!!
#    'recommendation': get_recommendation()}
#    return make_response(jsonify(data))

if __name__ == "__main__":
    #app.run(debug=True, port=5000)
    app.run()