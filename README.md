# Django Boilerplate
This project contains some boilerplate code that almost every project needs to be
implemented.

# Installation Process
1. Clone the project or download the project as zip file. If you have downloaded
   the zip file then extract the zip file to you desired location.
2. Create a virtual environment. It is always a good idea to create and work with
   virtual environment. You can use python's builtin module or any wrapper of this
   module such as ``virtualenv``, ``pipenv``, ``poetry`` etc. In this project, I
   have used ``virtualenv``. If you are using that too, then you can run the command
   below.
```commandline
virtualenv venv --python 3.8
```
3. Activate the virtual environment by running the command as follows.

For *Linux* or *Mac* user
```commandline
source venv/bin/activate
```

For *Windows* user
```commandline
venv\Scripts\activate
```
4. Install required python packages by running
```commandline
pip install -r requirements.txt
```

# Install Postgresql
If you are using *Linux* or *Mac*, then you can use your package manager to install
postgresql database on your system. For *Linux*, you can run
```commandline
sudo apt install postgresql postgresql-contrib
```
For *Mac*, you will get similar command with ``brue``.

For *Windows* user, you can download the installer file from [here](https://www.postgresql.org/).

# Create a Database for Your Project
If you are using *Linux* or *Mac*, then you can follow the steps to create a new
database for your project.
1. Run ``sudo -u postgresql psql``
2. Then you can run ``\l`` to list all available databases. *(Optional)*
3. Run the following command to create a new database for your project.
```commandline
CREATE DATABASE mydb;
```
4. Create a new user for your database. For that, just run 
```commandline
CREATE USER myuser WITH ENCRYPTED PASSWORD 'password';
```
5. Modify the role of this user.
```commandline
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed'
ALTER ROLE myuser SET timezone TO 'UTC'
ALTER USER myuser CREATEDB
```
6. Grant all permission fof ``mydb`` to ``myuser``.
```commandline
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```
7. Everything has been set now. To exist out of *postgres console* run ``\q``.

# Write Configuration File
1. Create a file called **config.ini** in root of your project.
*(where the manage.py file is)*
2. Create a sections as below and modify it as per your need.
```commandline
[Database]
NAME = mydb
USER = myuser
PASSWORD = password
HOST = localhost
PORT = 5432

[Secret]
KEY = SuperSecreteKey123!@#
```

# Migrate Your Database
To migrate your database, you just need to run the following command.
```commandline
python manage.py migrate
```
Now you are all set and ready to go. Now you can run server by running
``python manage.py runserver``
