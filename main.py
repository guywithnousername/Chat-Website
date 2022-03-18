from flask import render_template as rend
from flask import *
from flask_mail import *
import re
import random
import os
import string
import sqlite3
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from database import *
from chat import chatpage
from user import userpage

app = Flask(__name__)
app.register_blueprint(chatpage)
app.register_blueprint(userpage)
app.config['TESTING'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mldu@cydu.net'
app.config['MAIL_PASSWORD'] = 'LTb#s7EC8SRl$pPpcD'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.secret_key = '9ac7d06219fbfa373f76c9a6be47b178157e2a91436b263b703c63246e25'
mail = Mail(app)
DATABASE = "database.db"


def check_box():
    with app.app_context():
      con = get_db()
      cur = con.cursor()
      now = datetime.datetime.now()
      if (now.minute == 0):
        if (now.hour % 2 == 1):
            cur.execute("UPDATE Coins SET Box = 1")
        else:
            cur.execute("UPDATE Coins SET Box = 0")
        con.commit()


@app.route("/",methods= ["GET","POST"])
def index():
    name = request.cookies.get("Username")
    if request.cookies.get("Username") == None:
        return rend("index.html")
    else:
        con = get_db()
        cur = con.cursor()
        now = datetime.datetime.now()
        coins = query_db("SELECT Num FROM Coins WHERE Username = ?",(name,),one=True)
        if not coins: coins = 0
        else: coins = coins["Num"]
        bio = query_db("SELECT * FROM Users WHERE Username = ?",(name,),one=True)
        if not bio: bio = "You do not have a bio."
        else: bio = bio["Bio"]
        friends = [x["Friend1"] if x["Friend1"] != name else x["Friend2"] for x in query_db("SELECT * FROM Friends WHERE (Friend1 = ? OR Friend2 = ?) AND Code = 'confirmed'",(name,name))]
        box = query_db("SELECT Box FROM Coins WHERE Username = ?",(name,),one=True)
        if not box: box = False
        else: box = bool(box["Box"])
        ret = cur.execute("SELECT * FROM UserMessages WHERE Recipient = ? AND Read = 0",(name,))
        mess = len([0 for x in ret])
        return rend("user.html",name=name,friends=friends,coins=coins,bio=bio,isbox=box,mess=mess)

@app.route("/register",methods = ['GET','POST'])
def reg():
    name = request.cookies.get("Username")
    if name:
        return rend("message.html",message = "Log out first")
    if request.method == "POST":
        name = request.form.get("name")
        if ' ' in name:
            return rend("message.html",message="Names cannot have spaces."), 401
        password = request.form.get("password")
        if len(password) < 8:
            return rend("message.html",message="Your password is not strong enough."), 401
        e_mail = request.form.get("email")
        if not (re.match("^\S+@\S+\.\S+$",e_mail)):
            return rend("message.html",message="Invalid email")
        randomcode = (''.join(random.choice(string.digits) for i in range(1,15)))
        con = get_db()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            ret = cur.execute("""
            INSERT INTO Users (Username, Pass, Random)
            VALUES (?,?,?);
            """,(name.title(),password,randomcode))
            con.commit()
        except Exception as e:
            print(e)
            return rend("message.html",message="That username is taken."),403
        finally:
            cur.execute("INSERT INTO Coins (Username, Num, Box) VALUES (?, 1, 1)",(name.title(),))
            con.commit()
            con.close()
        email(rend("confirm.html",link=randomcode),recipients=[e_mail])
        return rend("message.html", message="Great! You created an account. To verify it, go to your email and click the link.")
    return rend("nameform.html",type='Register',email=True)

@app.route("/login",methods = ['GET','POST'])
def login():
    name = request.cookies.get("Username")
    if name:
        return rend("message.html",message="Log out first.")
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        con = get_db()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Users WHERE Username = ?",(name.title(),))
        ret = cur.fetchone()
        if ret == None:
            return rend("message.html",message="The username has been entered incorrectly.")
        else:
            if ret['Random'] != 'confirmed':
                return rend("message.html",message="You have not confirmed your account.")
            if ret['Pass'] == password:
                resp = make_response(redirect("/"))
                resp.set_cookie("Username",name.title())
                return resp
            else:
                return rend("message.html",message="You have entered the password incorrectly.")
    return rend("nameform.html",type="Login to your account")

@app.route("/logout",methods = ['GET','POST'])
def logout():
    name = request.cookies.get("Username")
    if name == None:
        return rend("message.html",message = "You aren't logged in.")
    if request.method == "POST":
        resp = make_response(rend("message.html",message="You have been successfully logged out"))
        resp.set_cookie('Username', '', expires=0)
        return resp
    return rend("logout.html")

@app.route("/confirm/<name>")
def confirmname(name):
    con = get_db()
    cur = con.cursor()
    sel = cur.execute("SELECT * FROM Users WHERE Random = ?",(name,)).fetchone()
    if (name == "confirmed"):
        return rend("message.html",message="Stop trying to target weaknesses in the code!")
    if (sel == None):
        return rend("message.html",message="The code was entered incorrectly.")
    cur.execute("""
    UPDATE Users
    SET Random = 'confirmed'
    WHERE Username = ?
    """,(sel['Username'],))
    con.commit()
    con.close()
    return rend("message.html",message="Your account has been confirmed! Now login to your account.")

def email(html,recipients=['mldu@cydu.net']):
    msg = Message("Email",
    sender="mldu@cydu.net",
    recipients=recipients)
    msg.html = html
    mail.send(msg)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



if __name__ == "__main__":
    from waitress import serve
    init_db()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_box, trigger="interval", seconds=60)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    port = int(os.environ.get('PORT', 8080))
    serve(app, host="0.0.0.0", port=port)
