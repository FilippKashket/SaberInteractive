Test task for "Saber Interactive"

WARNING! This service uses cookies for identifying clients, 
you must turn it on client

1. Install packages for project

$ virtualenv NEWVIRTUALENV
$ source NEWVIRTUALENV/bin/activate
$ pip install -r requirements.txt

2. Customization

There are two variables in server.py script
file_name = "'test1.txt'" - name of file with log
lines_in_message = 1000 - quantity of lines in one response

2. For run use

python server.py

Running on http://127.0.0.1:3000/
