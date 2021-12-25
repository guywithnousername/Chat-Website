from flask import render_template as rend
from flask import *
from datetime import datetime
import sqlite3
from database import *
from cryptography.fernet import Fernet

app = Flask(__name__)
DATABASE = "database.db"
app.secret_key = '9ac7d06219fbfa373f76c9a6be47b178157e2a91436b263b703c63246e25'
cryptokey = b'RwdEWFPygOggOdXRkNSKGM8Wm58QT6ZIpZ34oauwkSE='
fernet = Fernet(cryptokey)

@app.route("/")
def index():
    return rend("index.html")

@app.route("/register",methods = ['GET','POST'])
def reg():
    init_db()
    if request.method == "POST":
        name = request.form.get("name")
        if ' ' in name:
            return rend('message.html',message="Names cannot have spaces."), 401
        password = request.form.get("password")
        if len(password) < 8:
            return rend('message.html',message="Your password is not strong enough."), 401
        con = get_db()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            ret = cur.execute("""
            INSERT INTO Users (Username, Pass)
            VALUES (?,?);
            """,(name.title(),password))
            con.commit()
        except Exception as err:
            return rend('message.html',message="That username is taken."),403
        finally:
            con.close()
        return rend('message.html', message="Great! You created an account. To verify it, go to the login page and log in.")
    return rend('usernameform.html',type='Register')

@app.route("/login",methods = ['GET','POST'])
def login():
    init_db()
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        con = get_db()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Users WHERE Username = ?",(name.title(),))
        ret = cur.fetchone()
        if ret == None:
            return rend('message.html',message="The username has been entered incorrectly.")
        else:
            if ret['Pass'] == password:
                resp = make_response(rend('user.html', name=name.title(),password=password))
                resp.set_cookie("Username",name.title())
                return resp
            else:
                return rend("message.html",message="You have entered the password incorrectly.")
    return rend('usernameform.html',type="Login to your account")

@app.route("/chatroom/<room>",methods = ['GET','POST'])
def chat(room):
    init_db()
    con = get_db()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    encryptedroomname = bytes(request.cookies.get("Room"),'utf-8')
    decodedroom = fernet.decrypt(encryptedroomname).decode()
    if (room != decodedroom):
        return rend("message.html",message="You cannot access this room.")
    if request.method == "POST":
        message = request.form.get("message")
        name = request.cookies.get("Username") or 'Unnamed'
        time = datetime.now().strftime("%B %d, %Y %I:%M%p")
        cur.execute("""
        INSERT INTO Messages (RoomName,MSG,Username,Timestamp)
        VALUES (?,?,?,?)
        """, (room.title(),message,name,time))
        con.commit()
    select = query_db("""
        SELECT MSG,Username,Timestamp FROM Messages
        WHERE RoomName = ?
        ORDER BY Timestamp
        """,(room.title(),))
    con.close()
    select = [(x[0],x[1],x[2]) for x in select]
    return rend("room.html",messages=select)

@app.route("/roomselect",methods=['GET','POST'])
def selrooms():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        con = get_db()
        cur = con.cursor()
        cur = cur.execute("SELECT Pass FROM Rooms WHERE RName = ? ", (name.title(), ))
        ret = cur.fetchone()
        if not ret:
            return rend("message.html",message=f"The room {name.title()} was not found.")
        if ret['Pass'] != password: 
            return rend("message.html",message="The password was wrong.")
        resp = make_response(redirect(f"/chatroom/{(name.title())}",code=302))
        resp.set_cookie('Room',fernet.encrypt(name.title().encode()))
        return resp
    return rend("usernameform.html",type="Join a room")

@app.route("/logout",methods = ['GET','POST'])
def logout():
    if request.method == "POST":
        resp = make_response(rend("message.html",message="You have been successfully logged out"))
        resp.set_cookie('Username', '', expires=0)
        return resp
    return rend('logout.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



if __name__ == "__main__":
	from waitress import serve
	print("Serving at http://192.168.86.23:8000/ . . .")
	serve(app, host="0.0.0.0", port=8000)