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

def checkIfIn(cookie): # had to add because circular import error
    con = database.get_db()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if not cookie:
        return False
    cookie =  bytes(cookie, 'utf-8')
    try:
        decoded = fernet.decrypt(cookie).decode("utf-8");
    except:
        return False
    select = database.query_db("""
        SELECT Username FROM Users
        WHERE Username = ?
        """,(decoded,), one=True)
    return select[0]

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
        message = re.sub(r"\*\*(.+)\*\*",r"<strong>\1</strong>",message)
        message = re.sub(r"__(.+)__",r"<i>\1</i>",message)

        anon = 0
        name = request.cookies.get("Username")
        name = checkIfIn(name)
        if not name:
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
    username = request.cookies.get("Username")
    username = checkIfIn(username)
    if not username:
        return rend("message.html", message="You aren't logged in.")
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
    content2 = content
    con = database.get_db()
    cur = con.cursor()
    user = request.cookies.get("Username")
    sel = database.query_db("SELECT * FROM Block WHERE Blocker = ? AND Blocked = ?",args = (recipient,user),one = True)
    time = int(datetime.now().strftime("%s"))
    if sel != None:
        othermess = "Your message to ' " + recipient + " ' was blocked on the way."
        content2 = "A blocked user, ' " + user + " ', sent you a message, but it was blocked."
        cur.execute("INSERT INTO UserMessages (Recipient,MSG,Time,Read) VALUES (?,?,?,0)",(user,othermess,time))
    cur.execute("INSERT INTO UserMessages (Recipient,MSG,Time,Read) Values (?,?,?,0)",(recipient,content2,time))
    con.commit()

@chatpage.route("/confirmfriend/<code>")
def confirm(code):
    name = request.cookies.get("Username")
    name = checkIfIn(name)
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

@chatpage.route("/unblock/<name>",methods = ["GET","POST"])
def unblock(name):
    user = request.cookies.get("Username")
    user = checkIfIn(user)
    if not user:
        return rend("message.html",message = "You aren't logged in.")
    if request.method == "POST":
        con = database.get_db()
        cur = con.cursor()
        sel = database.query_db("SELECT * FROM Block WHERE Blocker = ? AND Blocked = ?",args = (user,name),one=True)
        if sel == True:
            return rend("message.html",message = "You haven't even blocked that user.")
        cur.execute("DELETE FROM Block WHERE Blocker = ? AND Blocked = ?",(user,name))
        con.commit()
        con.close()
        return rend("message.html",message = "Unblocked.")
    return rend("unblock.html",name=name)

@chatpage.route("/transfer",methods = ['GET','POST'])
def transfer():
    n = request.cookies.get("Username")
    n = checkIfIn(n)
    if not n:
        return rend("message.html",message = "You aren't logged in.")
    con = database.get_db()
    cur = con.cursor()
    coins = database.query_db("SELECT Num FROM Coins WHERE Username = ?",args=(n,),one=True)["Num"]
    if request.method == "POST":
        user = request.form.get("user").title()
        sel = database.query_db("SELECT * FROM Users WHERE Username = ?",args=(user,))
        if sel == None:
            return rend("message.html",message="That user doesn't exist.")
        password = request.form.get("pass")
        confirm = database.query_db("SELECT Pass FROM Users WHERE Username = ?",args=(n,),one=True)["Pass"]
        if confirm != password:
            return rend("message.html",message="Wrong password.")
        num = request.form.get("num")
        try:
            num = int(num)
        except:
            return rend("message.html",message="Invalid number.")
        if not num or num <= 0 or num > coins:
            return rend("message.html",message="Invalid number.")

        sel = database.query_db("SELECT Num FROM Coins WHERE Username = ?",args=(user,),one=True)
        if not sel:
            cur.execute("INSERT INTO Coins(Username,Num,Box) VALUES(?,?,1)",(user,num))
        else:
            cur.execute("UPDATE Coins SET Num = ? WHERE Username = ?",((sel["Num"] + num),user))
        cur.execute("UPDATE Coins SET Num = ? WHERE Username = ?",((coins - num),n))
        con.commit()
        con.close()
        return rend("message.html", message = "Transferred.")
    return rend("transfer.html",max=str(coins))
