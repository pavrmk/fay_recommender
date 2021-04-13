# News recommender bot "Fay" with Non-Negative Matrix Factorization

Final project for the [Spiced Data Science Bootcamp](https://www.spiced-academy.com/en/program/data-science) by [Pavel Romanenko](https://github.com/pavrmk). For this project Pavel took the live data with enterprise innovation projects from my website [Future Atelier](https://www.futureatelier.com/). Future Atelier is a database and newsletter which lists the most remarkable enterprise innovation projects. Based on the preferences of the newsletter subscribers of Future Atelier Pavel has created a recommender bot which can predict innovation projects a new user may like based on their input.

## Credits

[Malte Bonart](https://github.com/bonartm) created the [template](https://github.com/bonartm/heroku-flask) for deploying a Flask app to Heroku; and [Paul Wlodkowski](https://github.com/pawlodkowski) [adopted](https://github.com/pawlodkowski/heroku_flask_template) this template.

## Live version

A live version of this recommender bot is avaliable via https://fay-recommender.herokuapp.com/

PLEASE NOTE: The website may take some 20 seconds to load when you try to access it for the first time during your session. This is due to using a free tier Heroku server which goes to sleep when the website was not visited recently.

<kbd>
  <img src="https://github.com/futureatelier/fay_recommender/blob/main/images/readme_file_screenshots/fay_live.gif">
</kbd>

## Deployment 

For this demo version Pavel created a MySQL database with 100+ enterprise innovation projects. 

![MySQL Database Screenshot](https://github.com/futureatelier/fay_recommender/blob/main/images/readme_file_screenshots/database.png)

The information from this database is processed with Python and RegEx to get clean tags and URLs.

``` 
database['tags'] = database['tags'].replace('[?⚡⚽⚫✈️]', ',', regex = True) # Remove question marks which replcaed the emojis
database['tags'] = database['tags'].replace('[\U00010000-\U0010ffff]', ',', regex = True) # Remove all emojis
database['tags'] = database['tags'].replace(',,', ',', regex = True) # Remove double commas with single comma
database['tags'] = database['tags'].replace('\s*,\s*',', ', regex = True) # Remove the spacings before and after commas
database['tags'] = database['tags'].replace('(^..)','', regex = True) # !! This one should be replaced by a better regex or a for-loop to remove leading comma in a string
database['tags'] = database['tags'].replace('^\s+', '', regex = True) # Remove white space at the beginning of the string
database['tags'] = database['tags'].replace('[ \t]+$','', regex = True) # Remove white space at the end of the string
database['url'] = database['url'].replace('\?utm_source.+','', regex = True) # Remove the tracking link ?utm_source=Future+Atelier...
database['url'] = database['url'].replace('utm_source.+','', regex = True)
```

## Using the Non-Negative Matrix Factorization (NMF) for the recommendation engine

To get recommendations we are using the [Non-Negative Matrix Factorization](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html) from the sklearn.decomposition module.

To fit the model we need the usage data of the sample users who clicked on the news from the database. Based on this data we can create two matrices to train the model: one for the preferred URLs and one for the preferred tags. With this model we can predict the URLs and tags a new user may like, given one or more 

## To do

* Fix the mobile version of the demo website
