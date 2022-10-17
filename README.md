# Combining OCL and Natural Language: a Call for a Community Effort
The growing popularity and availability of pretrained natural language models opens the door to many interesting applications combining natural language (NL) with software artefacts. A couple of examples are the generation of code excerpts from NL instructions or the verbalization of programs in NL to facilitate their comprehension.

Many of these language models have been trained with open source software datasets and therefore “understand” a variety of programming languages, but not OCL.


We argue that OCL needs to jump into the machine learning bandwagon or it will risk losing its appeal as a constraint specification language. For that, the key first task is to create together an OCL corpus dataset amenable for natural language processing.


## Installation
- Install requirements.txt with pip
- Edit ocl/settings/local.py according to your database server. We asume is MYSQL, but you can also change that.
- Import the SOMSQL.sql to the database of the project. The actual .sql is dumpped from MYSQL.
- python manage.py runserver
- or you can use gunicorn to launch the service

You can also wrap the app with Docker and use .env vars instead to protect secrets. That's why you can find the ocl/settings/production.py in the repo and you can set it up accordingly.


# How to import the datasets from scratch
The repo has an SOMOCL.sql file to initialize the service with the datasets already migrated to MYSQL for you. But you can also modify the commands that work directly with the Spider and WikiSQL datasets.

Your MYSQL service should be installed and set up accordingly in ```ocl/settings/local.py'''

+ To migrate the original Spider dataset to the SOM dataset:
    - Download and unzip content to /data/spider
    - Exec: python manage.py migrateFromSpider migrateTables
    - Exec: python manage.py migrateFromSpider migrateQuestions
    - Exec: python manage.py migrateFromSpider migrateAssociations

+ To migrate the original WikiSQL dataset to the SOM dataset:
    - Download and unzip a copy to /data
    - Exec: python manage.py migrateFromWikiSQL migrate


Remember that the best way is to create a virtualenv and source activate it (using either virtualenv or Anaconda).

