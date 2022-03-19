# Chat Website
This will be a website where users can register, login, and chat with each other with private or public chat rooms. So far, we need to do these tasks in order to get it to work:
- [x] Style the page so it looks better (css)
- [ ] Add more functionality
- [ ] Host it with a server
- [ ] Add ads to the server
- [ ] Get people to view it

## Dependencies
This website uses:
- Flask (from flask import *)
- Cryptography (import cryptography.fernet)
- Waitress (from waitress import serve)
- Flask Mail (from flask_mail import *)
- Javascript Confetti (from [here](https://github.com/loonywizard/js-confetti))
in a .venv virtual environment.

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

## Virtual Environment
Don't forget to activate the venv virtual environment every time you run this with
```
. .venv/bin/activate
```
or
```
.venv/Scripts/activate
```
## Actually Running It
To run this, do 
```
python3 main.py
```
Then go to `localhost:8000`

and you should see the website.
