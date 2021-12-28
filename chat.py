from flask import *
from flask import render_template as rend
import database
import sqlite3
from cryptography.fernet import Fernet
from datetime import datetime

chatpage = Blueprint('chatpage',__name__,template_folder="templates",static_folder="static")
cryptokey = b'RwdEWFPygOggOdXRkNSKGM8Wm58QT6ZIpZ34oauwkSE='
fernet = Fernet(cryptokey)

@chatpage.route("/chatroom/<room>",methods = ['GET','POST'])
def chat(room):
    con = database.get_db()
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
        acttime = int(datetime.now().strftime("%s"))
        cur.execute("""
        INSERT INTO Messages (RoomName,MSG,Username,Timestring,Time)
        VALUES (?,?,?,?,?)
        """, (room.title(),message,name,time,acttime))
        con.commit()
        return redirect(f"/chatroom/{room}")
    select = database.query_db("""
        SELECT MSG,Username,Timestring FROM Messages
        WHERE RoomName = ?
        ORDER BY Time DESC
        """,(room.title(),))
    con.close()
    select = [(x[0],x[1],x[2]) for x in select]
    return rend("room.html",messages=select)

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
    return rend("usernameform.html",type="Join a room")