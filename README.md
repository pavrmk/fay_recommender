# News recommender bot "Fay" with non-negative matrix factorization (NMF)

## Credits

Final project for the [Spiced Data Science Bootcamp](https://www.spiced-academy.com/en/program/data-science).
Credits to [Malte Bonart](https://github.com/bonartm) who created the [template](https://github.com/bonartm/heroku-flask) for deploying a Flask app to Heroku; and [Paul Wlodkowski](https://github.com/pawlodkowski) who [adopted](https://github.com/pawlodkowski/heroku_flask_template) this template.

## Live version

A live version of this recommender bot is avaliable via https://fay-recommender.herokuapp.com/

PLEASE NOTE: The website may take some 20 seconds to load when you try to access it for the first time during your session. This is due to using a free tier Heroku server which goes to sleep when the website was not visited recently.

<kbd>
  <img src="https://github.com/futureatelier/fay_recommender/blob/main/images/readme_file_screenshots/fay_live.gif">
</kbd>

## Deployment 

For this demo version I created a MySQL database with 100+ enterprise innovation projects. 

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
