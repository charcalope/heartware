#!/bin/bash

source flask_venv/bin/activate

export FLASK_APP=server.py
export FLASK_ENV=development

echo -e "\u001b[5m Starting Heartware web server...\u001b[0m"
echo -e "\u001b[31m  ▄█████▄   ▄█████▄  "
echo -e "\u001b[31m ▄█████████████████▄ "
echo -e "\u001b[31m ███████████████████ "
echo -e "\u001b[31m ████▓▓▓▓▓▓▓▓▓▓▓████ "
echo -e "\u001b[31m ████▓\u001b[37mHeartware\u001b[31m▓████ "
echo -e "\u001b[31m ████▓▓▓▓▓▓▓▓▓▓▓████ "
echo -e "\u001b[31m █████▓\u001b[37mv0.0.1\u001b[31m▓▓█████ "
echo -e "\u001b[31m █████▓▓▓▓▓▓▓▓▓█████ "
echo -e "\u001b[31m  █████████████████  "
echo -e "\u001b[31m   ███████████████   "
echo -e "\u001b[31m    █████████████    "
echo -e "\u001b[31m     ███████████     "
echo -e "\u001b[31m      ▀███████▀      "
echo -e "\u001b[0m" 
echo -e "\u001b[4m -- Starting Heartware web server... -- \u001b[0m\n"

flask run --host=0.0.0.0 -p 8080 

deactivate
