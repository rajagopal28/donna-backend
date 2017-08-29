# Donna Backend API server
To bring in contextual references with the existing system at [Donna](http://github.com/rajagopal28/Donna)
## tech stack
- python - Flask, SQLAlchemy
- SQLite

## Libraries used
- Flask - application module to serve application with wnd points
- Flask-SQLAlchemy - ORM module to handle DB responses
- requests - to handle external requests

## Reasons for choosing Flask
- had previous experience with Python Flask
- easy to build api based platform
- quick to setup in mac/linux environments
- good for smaller applications like this

## Steps to run the application
### installing the packages
- `` cd donna-backend ``
- run the command `` pip install --upgrade -r requirements.txt ``
- use `` sudo `` if fails with permission issues

### running server
- `` python run-local.py ``

### running integration tests
- `` python run-tests.py ``

### end points information
- GET /api/users  - to list all active users
- POST /api/users {firstName: .., lastName: .., username:.., password: .., location: ..} - to add a new user
- GET /api/users/:user-id - to get detail of given user-id
