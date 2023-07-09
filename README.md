# ChickoMenu
Digital Menu Genrator
 

Not finished yet !

[ Sample Front ](https://github.com/younes-nb/chicko-frontend)

# Django Digital Menu Genrator 

## Setup

clone the repository:

```sh
$ git clone https://github.com/oldcorvus/ChickoMenu.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements/development.txt
```


Once `pip` has finished downloading the dependencies:
create two .env files  in root of project

sample .env
```sh
# تنظیمات Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# تنظیمات Flower
FLOWER_PORT=5555
FLOWER_BASIC_AUTH=username:password
```

sample .env.db
```sh
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
POSTGRES_DB = ChickoMenu

```

create another .env file in ChickoMenu/settings/

sample .env

```sh
DEBUG=yes
SECRET_KEY=django-insecure-czqrclgp!r826lvv19$8vpp6rky9#whlcp(epqzv$q8q!ex@$i
DATABASE_URL=psql://chickomenu:chikomenu@127.0.0.1:5430/chikomenu
STATIC_URL=/static/
API_KEY=
DB_HOST=db
DB_NAME=app
DB_USER=postgres
DB_PASS=supersecretpassword

```
and to run development server locally

```sh
(env)$ python manage.py runserver --settings=ChickoMenu.settings.development

```
And navigate to `http://127.0.0.1:8000/`.


## Running Locally with Docker

1.build the image:

```sh
  $ docker-compose build .
```
2.Spin up the containers
```sh
  $ docker-compose up
```
then view the site at  http://localhost:8000/

## Important

It is important to change sensitive information such as secret keys and API keys before deploying your application to production. Leaving default or test values in production can make your application vulnerable to security risks such as data breaches and unauthorized access

Generate a new secret key for your Django application using a cryptographically secure random generator. You can do this by running
```sh
 python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())
 ```
 
in your terminal and replacing the SECRET_KEY value in your settings file with the new key.

## Tests

To run the tests:
```sh
(env)$ python manage.py test --settings=ChickoMenu.settings.development
```
and for docker 

```sh
(env)$ docker-compose run web python manage.py test  --settings=ChickoMenu.settings.development

```
## API Docs 
  navigate to `http://127.0.0.1:8000/swagger/`
  navigate to `http://127.0.0.1:8000/redoc/`

  
## Features
 user plan,
 otp authentications, 
 token based  authentication,
 
