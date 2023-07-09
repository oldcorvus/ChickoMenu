# ChickoMenu Digital Menu Generator

**Note: This project is not finished yet!**

Check out the [sample front-end](https://github.com/younes-nb/chicko-frontend).

# Setup

1. Clone the repository:

```sh
$ git clone https://github.com/oldcorvus/ChickoMenu.git
```

2.Create a virtual environment and activate it:

```sh
$ virtualenv env
$ source env/bin/activate
```

3.Install the required dependencies:

```sh
(env)$ pip install -r requirements/development.txt
```
# Environment Variables

After pip has finished downloading the dependencies, create the following two .env files in the root of the project:

## sample .env file:

```sh
# Celery Settings
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Flower Settings
FLOWER_PORT=5555
FLOWER_BASIC_AUTH=username:password
```

## sample .env.db file:

```sh
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
POSTGRES_DB = ChickoMenu

```

Create another .env file in ChickoMenu/settings/ with the following environment variables:

## Sample .env file:

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
These variables are needed for the project to run correctly, and should be customized for your specific environment.

# Running the Development Server

To run the development server locally, use the following command:

```sh
(env)$ python manage.py runserver --settings=ChickoMenu.settings.development

```
Then, navigate to http://127.0.0.1:8000/ in your web browser to view the site.

# Running Locally with Docker
If you prefer to run the application using Docker, follow these steps:


1.Build the Docker image:

```sh
  $ docker-compose build .
```
2.Spin up the containers:

```sh
  $ docker-compose up
```
Once the containers are running, you can view the site at http://localhost:8000/.

# Important

It is important to change sensitive information such as secret keys and API keys before deploying your application to production. Leaving default or test values in production can make your application vulnerable to security risks such as data breaches and unauthorized access

Generate a new secret key for your Django application using a cryptographically secure random generator. You can do this by running
```sh
 python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())
 ```
 
in your terminal and replacing the SECRET_KEY value in your settings file with the new key.

# Running Tests

To run the tests locally, use the following command:

```sh
(env)$ python manage.py test --settings=ChickoMenu.settings.development
```

If you are using Docker, use the following command instead:

```sh
(env)$ docker-compose run web python manage.py test  --settings=ChickoMenu.settings.development

```
This will run the test suite and output the results in the console. Use this to ensure that code is functioning properly and to catch any errors before deploying to production.


# API Documentation

To view the API documentation, navigate to:

http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
  
# Features

The ChickoMenu digital menu generator includes the following features:

User plan
Catch for menu views
OTP authentication
Token-based authentication
Celery 
...

These features enhance the functionality and security of the application.
