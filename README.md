# SWE574

This Repository contains the Term Project of SWE574 class in Bogazici Univesity.\
![QA-Tests](https://github.com/SWE-574-GROUP-1/SWE574-GROUP-1/actions/workflows/qa_test.yml/badge.svg)
![Unit-Tests](https://github.com/SWE-574-GROUP-1/SWE574-GROUP-1/actions/workflows/unit_test.yml/badge.svg)
![Deploy](https://github.com/SWE-574-GROUP-1/SWE574-GROUP-1/actions/workflows/deploy.yml/badge.svg)
## Authors:

- **Dağlar Berk Erdem**
- **Hüseyin Aydın**
- **Kaan Can**
- **Ertan Kaya**
- **Gencay Polat**
- **Eren Ohtaroğlu**
- **Damla Alkan**
- **Ali Kenan Yağmur**

## Application

The application is not in production for now.

## Introduction

LinkMe is a web based note-taking and posting application. Users can share, categorize contents from social media or
blogs and interact with other users
through contents. Moreover, users can browse through spaces or tags to discover contents in a specific area.

## Installation

Clone this git repository by using the command:

```
git clone https://github.com/SWE-574-GROUP-1/SWE574-GROUP-1
```

## Setup

Important Notes:

- Suggested version of Python is Python 3.8.
- Run the following commands in your GIT Bash terminal.

### Creating Virtual Environment

Open your GIT Bash terminal.\
Go to root directory and install virtualenv package to your global environment with following commands:

```
cd
pip install virtualenv
```

Create a virtual environment with following command:

```
virtualenv --python="</path/to/python.exe>" "</path/to/new/virtualenv/>"
```

Activate your virtual environment with following command:

```
source "</path/to/new/virtualenv>/scripts/activate"    ->This command is for Mac
.\Scripts\activate   -> This command is for Windows enviroment
```

Install site packages from requirements.txt with the following command:

```
pip install -r requirements.txt
```

### Local Run

Open the root directory of the project and execute the following command with terminal in order to run local server:

```
# Run from terminal
python manage.py runserver
# Run with docker
docker-compose up --build
```

To reach the web application go to **http://127.0.0.1:8000**.

### How to Run Tests

In this section, local run of Unit and QA tests is explained.\
Please make sure that the application is up and running. (See section 'Local Run')\
Please make sure that tests are performed in test database, NOT PRODUCTION.

#### Unit Tests

The application
Make sure that you are at the same directory with manage.py

```
# Local run
cd SWE574
python manage.py test
# docker alternative 1, go into container shell and run tests
docker exec -it SWE574 sh
python manage.py test
# docker alternative 2, run from terminal
docker exec -it SWE574 sh -c "python manage.py test"
```

A common error that may be encountered while creating new unit tests is,

- A test may raise an error, this cause django not to delete objects that are created through tests from database.\
  Suggested solution is to flush the database (Note that this is your test database):

```
# For local run
python manage.py flush  # Say yes to the upcoming prompt
# docker alternative 1, go into container shell and flush db
docker exec -it SWE574 sh 
python manage.py flush 
# docker alternative 2, run from terminal
docker exec -it SWE574 sh -c "python manage.py flush"  # Say yes to the upcoming prompt
```

#### QA Tests

Make sure that the virtual environment build with requirements_dex.txt.\
Go to the root directory of project and run following from terminal

```
# For flake8
pip install flake8
flake8
# For coverage report in docker
docker exec -it SWE574 sh -c "pip install coverage && coverage run manage.py test && coverage rep
ort && coverage html"
## Command above will create a directory called htmlcov through volumes 
## Open the index.html and manage_py.html reports with your browser  
```
