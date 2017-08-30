# Donna Backend API server
To bring in contextual references with the existing system at [Donna](http://github.com/rajagopal28/Donna)
## tech stack
- python - Flask, SQLAlchemy
- SQLite

## Libraries used
- Flask - application module to serve application with end points
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
#### Users
- GET /api/users  - to list all active users
- POST /api/users {firstName: .., lastName: .., username:.., password: .., location: ..} - to add a new user
- POST /api/users/login {username:.., password: ..} - to add a authenticate and get user token
- GET /api/users/:user-id - to get detail of given user-id
- GET /api/users/download - to download as user info as .json file
- POST /api/users/upload {users: FILE_STREAM(users.json)} - to upload users from .json file



#### Location
- GET /api/locations  - to list all locations
- POST /api/locations {name:..., latitude:..., longitude:..., campusId:...} - to add a new locations
- GET /api/locations/:location-id - to get detail of given location-id
- GET /api/locations/download - to download as locations info as .json file
- POST /api/locations/upload {locations: FILE_STREAM(locations.json)} - to upload locations from .json file

#### Campus
- GET /api/campus  - to list all campus
- POST /api/campus {name:..., latitude:..., longitude:...} - to add a new campus
- GET /api/campus/:campus-id - to get detail of given campus-id
- GET /api/campus/download - to download as campus info as .json file
- POST /api/campus/upload {campus: FILE_STREAM(campus.json)} - to upload campus from .json file
