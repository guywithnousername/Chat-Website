# Chat Website
This is a test website where I throw random features in.

## Dependencies
This website uses all the modules listed in the `requirements.txt` file in a .venv virtual environment.

# Running
## Downloading modules

To download them on Mac, do: (you also need to have python3)
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

To download them on Windows, do:
```
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python3 main.py
```
Also, to add all of the modules to `requirements.txt`,do:
```
pip freeze > requirements.txt
```

## Virtual Environment
Don't forget to activate the venv virtual environment every time you run this with
```
. .venv/bin/activate
```
or
```
.venv/Scripts/activate
```
in Windows
## Actually Running It
To run this, do 
```
python3 main.py
```
Then go to `localhost:8000`

and you should see the website.
