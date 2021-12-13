# Knightracker
This is the backend repo for [knightracker](https://github.com/knightSarai/weight-tracker-frontend) app.
Built using Django and Sqlite.

# API Endpoints
| Endpoint               | Description      | Methods  |
| -------------          |-------------     | -----|
| /admin/        | Access admin area    | GET  |
| /api/auth/csrf/        | Get csrf tocken    | GET  |
| /api/auth/login/       | User login        | POST |
| /api/auth/signup/      | User registration | POST |
| /api/auth/check-user-logged-in/      | See if client logged in or not | GET |
| /api/trainee/mesurements      | Get trainee measurements or add a new one | GET - POST |
| /api/trainee/mesurements/:id      | Get, edit, or delete a trainee measurement | GET - PUT - DELETE |

# Install Dependencies
First, you have to install [pip-tools](https://github.com/jazzband/pip-tools).
Then in the project directory run
```
pip-tools sync
```
# Run The Application
## Setup The Database
```
python manage.py migrate
```
## To Access The Admin Area
Create a super user
```
python manage.py createsuperuser
```
## Run The App
```
python manage.py runserver
```

# Future Works
- Allow trainers to login and monitor their trainee's measurements 
- Make more strict authentication rules.
- Increase the test coverage.

# Demo
A demo video can be seen [here](https://youtu.be/dXImDKTzbF0)
___
- Version: 0.1.0
- License: MIT
