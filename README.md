Test task for "Saber Interactive". Task description look at 'SaberPythonTest_new1.docx' 

WARNING! in this version offset and total_size are in bytes

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
