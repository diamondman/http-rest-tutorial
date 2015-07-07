## INTRO
This project aims to familiarize the reader with most of what goes into a modern web application.
It attempts to introduce the reader to:

* HTTP
  * Requests
  * Responses
  * Headers
  * How the browser sends HTTP Requests
  * How to send HTTP Requests with CURL (command line)
* RESTful Interfaces
  * GET/POST/PUT/DELETE Requests
  * GET and POST data
* Implementing a Python Webserver with Flask
  * Routes
  * Templates
  * Working with Requests and Responses
  * Databases and Object Relational Models (ORM)


## GETTING THE PROJECT
This project is maintained with git so the easiest way to get it is with the following command:
```
sudo apt-get install git
git clone https://github.com/diamondman/http-rest-tutorial.git
```
The previous command will copy all of this project's files, including this readme, into a new folder called 'http-rest-tutorial' on your computer. You are able to safely move this folder somewhere else after you copy it down from git. 

## INSTALL
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3 pip3 libsqlite3-0
sudo pip3 --upgrade install flask sqlalchemy flask-sqlalchemy ipython
```

## RUNNING
In the terminal run the following (replace things in { } with correct values)
```
cd {path to http-rest-tutorial}
./main.py
```
