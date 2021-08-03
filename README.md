# It Uses 
- python packages,
  - django==3.2.5
  - selenium==3.141.0
  - lxml==4.6.3
  - beautifulsoup4==4.9.3
  - requests==2.25.1
  - python-dotenv==0.19.0
  - dj-database-url==0.5.0
  - gunicorn==20.1.0
  - whitenoise==5.3.0
  - psycopg2>=2.8
- others,
  - jquery
  - chromedriver
  
---  


# Known Issues(2021-08-01)
- MAJOR ISSUE: "No web processes running" in Heroku -> solved!(2021-08-02)
- A common 4-tier architecture(development, testing, model, production) is ignored. 
- Alert: `clipper/views.py` can be abused !!!   
  but not activated yet due to the first issue.
- `Time out error` may occur.

---  
# Improvements or Changes(2021-08-01, slow_slow)
- `clipper/chromer.py` for common use of selenium chromedriver working.
- `clipper/jquery-3.6.0.min.js` added for webdriver to act with minimal errors.


# In `.env`
- `SECRET_KEY`
- `GOOGLE_CHROME_BIN` *오직 값없는 이름만.*
- `CHROMEDRIVER_PATH`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
---
# Perfomaces or Results
- Main command: `python start_clipper.py -n <site_name>`
- main command -> clipper/course_save.py -> <each_site>.py -> chromer.py
- Average 10-20 seconds for scraping a webpage.
  

# References
---  
- Xpath cheatsheet : https://devhints.io/xpath#indexing  
- Django Model URLField : https://docs.djangoproject.com/en/3.2/ref/models/fields/ 
- Supported Runtimes in Heroku: https://devcenter.heroku.com/articles/python-support#supported-runtimes  
- Heroku chromedriver buildpacks: https://github.com/heroku/heroku-buildpack-chromedriver
- How to deploy python selenium apps in Heroku: https://romik-kelesh.medium.com/how-to-deploy-a-python-web-scraper-with-selenium-on-heroku-1459cb3ac76c
- Deploying Django App on Heroku with Postgres: https://medium.com/@hdsingh13/deploying-django-app-on-heroku-with-postgres-as-backend-b2f3194e8a43