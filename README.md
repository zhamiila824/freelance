# Freelance
Freelance exchange web-site. Where customers can create tasks and put price. Executors can do task if it is not done and get paid.

# Installation and run
```
$ git clone https://github.com/zhamiila824/freelance.git
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
$ python manage.py sqlmigrate user 0001
$ python manage.py sqlmigrate task 0001
```

# URLs
http://127.0.0.1:8000/api/v1/users - List of users  
http://127.0.0.1:8000/api/v1/auth/sign_in - Login page  
http://127.0.0.1:8000/api/v1/auth/sign_up - Registration page  
http://127.0.0.1:8000/api/v1/tasks - List of tasks  
http://127.0.0.1:8000/api/v1/tasks/add - Create task  
http://127.0.0.1:8000/api/v1/tasks/<int:pk> - Task detail(pk is id of task)  

# Run tests
```
$ python manage.py test
```
