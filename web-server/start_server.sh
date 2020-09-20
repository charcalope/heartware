#!/bin/bash

source flask_venv/bin/activate

export FLASK_APP=server.py
export FLASK_ENV=development

flask run --host=0.0.0.0 -p 8080 

deactivate
