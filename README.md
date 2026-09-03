# CareBridge Hospital Web Application

This project upgrades the CareBridge Hospital Management System from a
command-line program into a Flask web application. It guides a patient through
four stages in order.

## Features

1. Register Patient and generate an urgent or non-urgent Patient ID.
2. Book an appointment and receive a doctor, clinic and booking reference.
3. Assign a triage room using a severity level from 1 to 10.
4. Calculate an itemised patient bill with the applicable subsidy discount.

## Technologies

- Python 3.12
- Flask
- HTML and CSS
- Git and GitHub
- Docker

## Run Locally

Install the required package:

```powershell
py -m pip install -r requirements.txt
```

Start the application:

```powershell
py app.py
```

Open `http://127.0.0.1:5000` in a web browser.

## Run with Docker

Build the image from the project folder:

```powershell
docker build -t carebridge-hospital .
```

Run the container:

```powershell
docker run --name carebridge-app -p 5000:5000 carebridge-hospital
```

Open `http://127.0.0.1:5000` in a web browser. Press `Ctrl+C` to stop the
container. To remove the stopped container, run:

```powershell
docker rm carebridge-app
```

## Docker Base Image

The project uses the assignment-required `python:3.12-alpine` base image.
