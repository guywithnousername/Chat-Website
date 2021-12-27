# Chat Website
This will be a website where users can register, login, and chat with each other with private or public chat rooms. So far, we need to do these tasks in order to get it to work:
- [ ] Style the page so it looks better (css)
- [ ] Add more functionality
- [ ] Host it with a server
- [ ] Add ads to the server
- [ ] Get people to view it

## Dependencies
This website uses:
- Flask (from flask import *)
- Cryptography (import cryptography.fernet)
- Waitress (from waitress import serve)
in a .venv virtual environment.

To download them on Mac, do: (you also need to have python3)
```
python3 -m venv .venv
. .venv/bin/activate
pip install Flask
pip install waitress
pip install cryptography
python3 main.py
```
To download them on Windows, do:
```
py -3 -m venv .venv
venv\Scripts\activate
pip install Flask
pip install waitress
pip install cryptography
python3 main.py
```