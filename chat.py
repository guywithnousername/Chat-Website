from flask import *
from flask import render_template as rend
import database
import sqlite3
from cryptography.fernet import Fernet
from datetime import datetime
import re
import htmlentities as h

chatpage = Blueprint('chatpage',__name__,template_folder="templates",static_folder="static")
cryptokey = b'RwdEWFPygOggOdXRkNSKGM8Wm58QT6ZIpZ34oauwkSE='
fernet = Fernet(cryptokey)

@chatpage.route("/chatroom/<room>",methods = ['GET','POST'])
def chat(room):
    con = database.get_db()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if not request.cookies.get("Room"):
        return rend("message.html",message="You cannot access this room.")
    encryptedroomname = bytes(request.cookies.get("Room"),'utf-8')
    decodedroom = fernet.decrypt(encryptedroomname).decode()
    if (room != decodedroom):
        return rend("message.html",message="You cannot access this room.")
    if request.method == "POST":
        message = h.encode(request.form.get("message"))
        message = re.sub(r"### (.+)", r"<h3>\1</h3>",message)
        message = re.sub(r"## (.+)", r"<h2>\1</h2>",message)
        message = re.sub(r"# (.+)", r"<h1>\1</h1>",message)
        message = re.sub(r"\[(.+)\]\(((https?://)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*)\)",r"<a href='\2'>\1</a>",message)

        anon = 0
        if request.cookies.get("Username"):
            name = request.cookies.get("Username")
        else:
            name = str(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr))
            anon = 1
        time = datetime.now().strftime("%B %d, %Y %I:%M%p")
        acttime = int(datetime.now().strftime("%s"))
        cur.execute("""
        INSERT INTO Messages (RoomName,MSG,Username,Timestring,Time,Anon)
        VALUES (?,?,?,?,?,?)
        """, (room.title(),message,name,time,acttime,anon))
        con.commit()
        return redirect(f"/chatroom/{room}")
    select = database.query_db("""
        SELECT MSG,Username,Timestring,Anon FROM Messages
        WHERE RoomName = ?
        ORDER BY Time DESC
        """,(room.title(),))
    con.close()
    select = [(x[0],x[1],x[2],x[3]) for x in select]
    return rend("room.html",rname=room,messages=select)

@chatpage.route("/roomselect",methods=['GET','POST'])
def selrooms():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        con = database.get_db()
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
    return rend("nameform.html",type="Join a room")

@chatpage.route("/newroom",methods=['GET','POST'])
def newroom():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if ' ' in name:
            return rend("message.html",message="Names cannot have spaces."), 401
        if len(password) < 8:
            return rend("message.html",message="Your password is not strong enough."), 401
        con = database.get_db()
        cur = con.cursor()
        try:
            cur = cur.execute("""
            INSERT INTO Rooms (RName,Pass)
            VALUES (?,?)
            """,(name.title(),password))
            con.commit()
        except:
            return rend("message.html",message="That name is taken.")
        finally:
            con.close()
        return rend("message.html",message="The room was successfully created.")
    return rend("nameform.html",type="Create a new room")

def mailboxmsg(recipient,content):
    con = database.get_db()
    cur = con.cursor()
    time = int(datetime.now().strftime("%s"))
    cur.execute("INSERT INTO UserMessages (Recipient,MSG,Time,Read) Values (?,?,?,0)",(recipient,content,time))
    con.commit()

@chatpage.route("/confirmfriend/<code>")
def confirm(code):
    name = request.cookies.get("Username")
    if code == "confirmed":
        return rend("message.html",message="Are you a hacker? If so, stop.")
    if not name:
        return rend("message.html",message="You aren't logged in.")
    con = database.get_db()
    cur = con.cursor()
    ret = cur.execute("SELECT * FROM Friends WHERE (Friend1 = ? OR Friend2 = ?) AND Code = ?",(name,name,code))
    if not ret:
        return rend("message.html",message="Wrong link.")
    cur.execute("UPDATE Friends SET Code = 'confirmed' WHERE Code = ?",(code,))
    con.commit()
    con.close()
    return rend("message.html",message="Successfully friended!")
