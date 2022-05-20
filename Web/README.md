# Milk pathogen predictions
Milk pathogen prediction service by Iker Silva/ Servicio de detección de patógenos en leche por Iker Silva.

Project developed with flask (Python 3.7+ needed)/ Proyecto desarrollado con flask (necesario Python 3.7+)

## In order to install requirements/ Para instalar las librerías necesarias:

    python -m pip install -r requirements.txt

## In order to execute the aplication/ Para ejecutar la aplicación:

open command line and execute/ abrir línea de comandos y ejecutar: 
    
	python run.py

## To acces the client side/ Para acceder a la parte cliente:

http://localhost:5000/

## To access the API (swagger)/ Para acceder a la API (swagger):

http://localhost:5000/api

## Functionality/ Funcionalidad:

-Not logged in:

    -Register new users
    -Login
    -Navigate through restaurant pages and see available products

-As a standard user:

    -Logout
    -Modify user information
    -Reser user password through email
    -Navigate through model pages
    -Select a model
    -Upload data
    -Obtain predictions
    -Check history of results

-As admin:

    -Logout
    -Navigate through model pages
    -Add new models
    -Modify existing models

