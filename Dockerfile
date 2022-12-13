FROM python:3.8

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip

RUN pip install --upgrade setuptools

RUN pip install ez_setup

RUN pip install -r requirements.txt

# COPY SWE573_Term_Project/* /app/
# COPY . .

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
