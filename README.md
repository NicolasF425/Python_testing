### gudlift-registration

## 1. Why

This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

## 2. Getting Started

This project uses the following technologies:

* Python v3.x+

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)

Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

* [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

This ensures you'll be able to install the correct packages without interfering with Python on your machine.

Before you begin, please ensure you have this installed globally. 


## 3. Installation

- After cloning, change into the directory and type _virtualenv -m venv_ This will then set up a a virtual python environment within that directory.

- Next, type source bin/activate (Linux) or venv\scripts\activate (Windows). You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type deactivate in place of activate in the command line.

- Rather than hunting around for the packages you need, you can install in one step. Type _pip install -r requirements.txt_. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is pip freeze > requirements.txt

- Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

## 4. Current Setup

The app uses [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
 
* competitions.json - list of competitions
* clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

## 5. Use and Testing

**For all actions, be in project directory and activate the virtual environnement**

**Runnig the application :**

In a terminal, lauch the application :

_flask --app server run_

Ctrl + click on the link  http://127.0.0.1:5000

**Run unit and integration tests**

Execute _pytest_ in project directory to lauch the unit test and integration tests

Execute _pytest --cov=._ to view test coverage

<img width="1886" height="932" alt="testsP11" src="https://github.com/user-attachments/assets/5b95b0ce-9d9c-46bd-bacb-9deb1a9186ea" />


**Performance tests :**

In another terminal, while the application is running :

execute _locust -f tests/performance_tests/locustfile.py_

ctrl + click on the link  http://localhost:8089

In the navigator enter the following parameters : 

number of users : 6

ramp up : 6

host : 127.0.0.1:5000
    
        



