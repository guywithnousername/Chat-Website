import database
from flask import *
from flask import render_template as rend
import random
import string
from chat import mailboxmsg as mailto

userpage = Blueprint('userpage',__name__,template_folder="templates",static_folder="static")

@userpage.route("/users/<name>",methods=['GET','POST'])
def viewuser(name):
    con = database.get_db()
    cur = con.cursor()
    name = name.title()
    cur.execute("SELECT * FROM Users WHERE Username = ?",(name,))
    sel = cur.fetchone()
    if sel == None:
        return rend("message.html",message="That user was not found.")
    coins = database.query_db("SELECT Num FROM Coins WHERE Username = ?",(name,),one=True)
    if not coins: coins = 0
    if coins: coins = coins["Num"]
    friends = [x["Friend1"] if x["Friend1"] != name else x["Friend2"] for x in database.query_db("SELECT * FROM Friends WHERE (Friend1 = ? OR Friend2 = ?) AND Code = 'confirmed'",(name,name))]
    username = request.cookies.get("Username")
    if username == name:
        return redirect("/")
    friend = cur.execute("SELECT * FROM Friends WHERE ((Friend1 = ? AND Friend2 = ?) OR (Friend2 = ? AND Friend1 = ?)) AND Code = 'confirmed'",(username,name,username,name)).fetchone()
    if request.method == "POST" and friend:
        cur.execute("DELETE FROM Friends WHERE ((Friend1 = ? AND Friend2 = ?) OR (Friend2 = ? AND Friend1 = ?)) AND Code = 'confirmed'",(username,name,username,name))
        con.commit()
        con.close()
        return rend("message.html",message = "That friend was unfriended.")
    return rend("userpage.html",name=name,bio=sel["Bio"],friend=friend,coins=coins,friends=friends)

@userpage.route("/change/profile",methods = ['GET','POST'])
def changeprof():
    name = request.cookies.get("Username")
    if name == None:
        return rend("message.html",message="You aren't logged in.")
    con = database.get_db()
    cur = con.cursor()
    bio = cur.execute("SELECT * FROM Users WHERE Username = ?",(name,)).fetchone()["Bio"]
    if (request.method == "POST"):
        new = request.form.get("bio")
        cur.execute("""
        UPDATE Users
        SET Bio = ?
        WHERE Username = ?
        """,(new,name))
        con.commit()
        return rend("message.html",message="Your bio was successfully updated!")
    con.close()
    return rend("changeprof.html",name=name,bio=bio)

@userpage.route("/change/password",methods = ['GET','POST'])
def changepass():
    name = request.cookies.get("Username")
    if name == None:
        return rend("message.html",message="You aren't logged in.")
    if request.method == "POST":
        password = database.query_db("SELECT * FROM Users WHERE Username = ?",args=(name,),one=True)["Pass"]
        oldpass = request.form.get("pass")
        pass1 = request.form.get("newpass")
        pass2 = request.form.get("newpass2")
        if (oldpass != password):
            return rend("message.html",message="You entered your old password incorrectly")
        if (pass1 != pass2):
            return rend("message.html",message="You entered your new passwords incorrectly")
        con = database.get_db()
        database.query_db("UPDATE Users SET Pass = ? WHERE Username = ?",args=(pass1,name))
        con.commit()
        con.close()
        return rend("message.html",message="Your password was changed successfully!")
    return rend("changepass.html")

@userpage.route("/newfriend",methods=['GET','POST'])
def addfriend():
    name = request.cookies.get("Username")
    if name == None:
        return rend("message.html",message="You aren't logged in.")
    if request.method == 'POST':
        con = database.get_db()
        cur = con.cursor()
        friend = request.form.get("friend").title()
        f = database.query_db("SELECT * FROM Friends WHERE (Friend1 = ? OR Friend2 = ?)",(friend,friend))
        if f:
            return rend("message.html",message="You either already have a friend request to or from that user, or already are friends with him or her.")
        sel = cur.execute("SELECT * FROM Users WHERE Username = ?",(friend,)).fetchone()
        if not sel:
            return rend("message.html",message="The user was not found.")
        randomcode = (''.join(random.choice(string.digits) for i in range(1,15)))
        mailto(friend,rend("friendmsg.html",code=randomcode))
        cur.execute("INSERT INTO Friends (Friend1, Friend2, Code) VALUES (?, ?, ?)",(name,friend,randomcode))
        con.commit()
        con.close()
        return rend("message.html",message="Requested.")
    return rend("newfriend.html")

@userpage.route("/messages")
def messages():
    name = request.cookies.get("Username")
    if not name:
        return rend("message.html",message="You aren't logged in.")
    con = database.get_db()
    cur = con.cursor()
    ret = cur.execute("SELECT * FROM UserMessages WHERE Recipient = ? ORDER BY Time DESC",(name,)).fetchall()
    msg = [(x["MSG"],x["Read"],str(x["ID"])) for x in ret]
    return rend("messages.html",msg=msg)

@userpage.route("/markread/<code>")
def markread(code):
    con = database.get_db()
    cur = con.cursor()
    ret = cur.execute("SELECT * FROM UserMessages WHERE ID = ?",(code,)).fetchone()
    if ret:
        cur.execute("UPDATE UserMessages SET Read = 1 WHERE ID = ?",(code,))
        con.commit()
        con.close()
    return rend("message.html",message="You aren't supposed to be here.")
@userpage.route("/addcoin/<user>")
def addcoin(user):
    name = request.cookies.get("Username")
    if not name:
        return rend("message.html",message="You aren't supposed to be here.")
    sel = database.query_db("SELECT Num FROM Coins WHERE Username = ?",(name,),one=True)
    con = database.get_db()
    cur = con.cursor()
    if not sel:
        cur.execute("INSERT INTO Coins (Username, Num, Box) VALUES (?, 1, 1)",(name,))
        con.commit()
    else:
        sel = int(sel["Num"]) + 1
        cur.execute("UPDATE Coins SET Num = ? WHERE Username = ?",(sel,name))
        con.commit()
    cur.execute("UPDATE Coins SET Box = 0 WHERE Username = ?",(name,))
    con.commit()
    con.close()
    return rend("message.html",message="You aren't supposed to be here.")
   
@userpage.route("/play")
def playgame():
    name = request.cookies.get("Username")
    if not name:
        return rend("message.html",message="You aren't logged in.")
    sel = database.query_db("SELECT Num FROM Coins WHERE Username = ?",(name,),one=True)
    if not sel or int(sel["Num"]) < 30:
        return rend("message.html",message="You do not have enough coins.")
    else:
        con = database.get_db()
        cur = con.cursor()
        sel = int(sel["Num"])
        sel -= 30
        cur.execute("UPDATE Coins SET Num = ? WHERE Username = ?",(sel,name))
        con.commit()
    con.close()
    return rend("play.html")
