commands - 
django-admin startproject medicserver
python manage.py startapp backend


packages installed -
pip install django 
pip install pytesseract
pip install openai
pip install python-dotenv
pip install requests
pip install opencv-python



django commands -
python manage.py runserver (requires settings.py file!!!)

for logs : 
    import logging

    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")
    lol= "123456789"
    logging.error('%s normal. Relax! %s',lol,42)


extra 
git update-index --assume-unchanged <filename>
#keep file in both remote and local, but dont track changes 

git rm --cached <filename>
git rm -r --cached <folder>
#remove the file from server, keep in local, stop tracking


ctrl+shift+p
terminus: open 


export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"

setting up steps: 

-> create a gcp service account, 
    create a config json file, set envVariable for it with path of the file 

    
