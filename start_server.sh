#!/bin/bash
clear

# Checking if venv folder exists and creating it if not, then installing requirements
if [[ ! -d "venv/" ]]
then
	echo "Venv not found! Creating..."
	python3 -m venv venv
	echo "Enabling venv..."
	source venv/bin/activate
	echo "Installing requirements from requirements.txt..."
	python3 -m pip install -u pip
	python3 -m pip install -r requirements.txt
	echo
	echo "Requirements installed! Starting heartware..."
	echo
else
	echo "Venv detected! Starting heartware..."
	source venv/bin/activate
	echo
fi

## Setting flask entry python file
export FLASK_APP=app.py
export FLASK_ENV=development

## Printing ASCII art
echo -e "\u001b[31m  ▄███████▄   ▄███████▄  "
echo -e "\u001b[31m ▄█████████████████████▄ "
echo -e "\u001b[31m ███████████████████████ "
echo -e "\u001b[31m ██████▓▓▓▓▓▓▓▓▓▓▓██████ "
echo -e "\u001b[31m ██████▓\u001b[37mHeartware\u001b[31m▓██████ "
echo -e "\u001b[31m ██████▓▓▓▓▓▓▓▓▓▓▓██████ "
echo -e "\u001b[31m ███████▓\u001b[37mv0.0.01\u001b[31m▓███████ "
echo -e "\u001b[31m ███████▓▓▓▓▓▓▓▓▓███████ "
echo -e "\u001b[31m  █████████████████████  "
echo -e "\u001b[31m   ███████████████████   "
echo -e "\u001b[31m    █████████████████    "
echo -e "\u001b[31m     ███████████████     "
echo -e "\u001b[31m      ▀███████████▀      "
echo
echo -e "\u001b[4mStarting Heartware web server...\u001b[0m"

## Printing hostname
echo "Hostname:" $(hostname -I)
echo

## Open web server IP if -o in script (only works on WSL, oops!)
if [[ $1 = "-o" ]]
then
	cmd.exe start /C "http://$(hostname -I | tr -d '[:space:]'):8080"
fi

## Starting flask
flask run --host=0.0.0.0 -p 8080 

deactivate
