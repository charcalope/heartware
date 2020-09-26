@echo off
cls

IF EXIST "venv\" (
    echo Venv detected! Starting heartware...
    call venv\Scripts\activate
    echo.
) ELSE (
    echo Venv not found! Creating...
    python3.exe -m venv venv
    echo Enabling venv...
    call venv\Scripts\activate
    echo Installing requirements from requirements.txt...
    pip install --upgrade pip
    pip install -r requirements.txt
    echo.
    echo Requirements installed! Starting heartware...
    echo.
)

:: Setting flask entry
set FLASK_APP=app.py
set FLASK_ENV=development

:: Printing ASCII art
echo     #####       #####
echo    #######     #######
echo   #####################
echo  #######################
echo  ######-----------######
echo  ######-Heartware-######
echo  ######-----------######
echo  #######-v0.0.01-#######
echo  #######---------#######
echo   #####################
echo    ###################
echo     #################
echo      ###############
echo        ###########
echo          #######
echo.
echo Starting Heartware web server...
echo.
flask run --host=0.0.0.0 -p 8080

deactivate
