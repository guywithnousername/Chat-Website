from flask import render_template as rend
from flask import *
from flask_mail import *
import sqlite3
from database import *
from chat import chatpage
from user import userpage

app = Flask(__name__)
app.register_blueprint(chatpage)
app.register_blueprint(userpage)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mldu@cydu.net'
app.config['MAIL_PASSWORD'] = 'LTb#s7EC8SRl$pPpcD'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
DATABASE = "database.db"
app.secret_key = '9ac7d06219fbfa373f76c9a6be47b178157e2a91436b263b703c63246e25'

@app.route("/",methods= ["GET","POST"])
def index():
    msg = Message("Email",
    sender="mldu@cydu.net",
    recipients=["mldu@cydu.net"])
    msg.body = "EEEEEMMMMMAAAAAIIIIILLLLL"
    mail.send(msg)
    name = request.cookies.get("Username")
    if request.cookies.get("Username") == None:
        return rend("index.html")
    else:
        return rend("user.html",name=name)

@app.route("/register",methods = ['GET','POST'])
def reg():
    if request.method == "POST":
        name = request.form.get("name")
        if ' ' in name:
            return rend("message.html",message="Names cannot have spaces."), 401
        password = request.form.get("password")
        if len(password) < 8:
            return rend("message.html",message="Your password is not strong enough."), 401
        con = get_db()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            ret = cur.execute("""
            INSERT INTO Users (Username, Pass)
            VALUES (?,?);
            """,(name.title(),password))
            con.commit()
        except:
            return rend("message.html",message="That username is taken."),403
        finally:
            con.close()
        return rend("message.html", message="Great! You created an account. To verify it, go to the login page and log in.")
    return rend("nameform.html",type='Register')

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
            return rend("message.html",message="The username has been entered incorrectly.")
        else:
            if ret['Pass'] == password:
                resp = make_response(redirect("/"))
                resp.set_cookie("Username",name.title())
                return resp
            else:
                return rend("message.html",message="You have entered the password incorrectly.")
    return rend("nameform.html",type="Login to your account")

@app.route("/logout",methods = ['GET','POST'])
def logout():
    if request.method == "POST":
        resp = make_response(rend("message.html",message="You have been successfully logged out"))
        resp.set_cookie('Username', '', expires=0)
        return resp
    return rend("logout.html")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



if __name__ == "__main__":
    from waitress import serve
    print("Serving at http://192.168.86.23:8000/ . . .")
    serve(app, host="0.0.0.0", port=8000)