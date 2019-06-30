# Freelance
Freelance exchange web-site. Where customers can create tasks and put price. Executors can do task if it is not done and get paid.

# Installation and run
```
$ git clone https://github.com/jamilya824/freelance.git
$ virtualenv venv -p python3
$ source venv/bin/activate
$ cd freelance
$ pip install -r requirements.txt
$ python manage.py runserver
```
Before running server:
1) create .env file in root directory with:
```
  SECRET_KEY=your_secret_key
```
2) make migrations:
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py sqlmigrate user 0001
$ python manage.py sqlmigrate task 0001
```
3) create superuser(to see admin page):
```
$ python manage.py createsuperuser
```