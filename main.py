from flask import Flask, request, render_template, g,make_response, url_for
import sqlite3
from database import *

app = Flask(__name__)
DATABASE = "database.db"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register",methods = ['GET','POST'])
def reg():
    init_db()
    if request.method == "POST":
        name = request.form.get("name")
        if ' ' in name:
            return render_template('message.html',message="Names cannot have spaces."), 401
        password = request.form.get("password")
        if len(password) < 8:
            return render_template('message.html',message="Your password is not strong enough."), 401
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
            return render_template('message.html',message="That username is taken."),403
        finally:
            con.close()
        return render_template('user.html', name=name.title(),password=password)
    return render_template('usernameform.html',type='Register')

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
            return render_template('message.html',message="The username has been entered incorrectly.")
        else:
            if ret['Pass'] == password:
                resp = make_response(render_template('user.html', name=name.title(),password=password))
                resp.set_cookie("Username",name)
                return resp
            else:
                return render_template("message.html",message="You have entered the password incorrectly.")
    return render_template('usernameform.html',type="Login to your account")

@app.route("/chatroom",methods = ['GET','POST'])
def chat():
    init_db()
    con = get_db()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if request.method == "POST":
        message = request.form.get("message")
        name = request.cookies.get("Username") or 'Unnamed'
        cur.execute("""
        INSERT INTO Messages (RoomName,MSG,Username)
        VALUES (?,?,?)
        """, ('family',message,
        name))
        con.commit()
    select = query_db("""
        SELECT MSG,Username,Timestamp FROM Messages
        WHERE RoomName = 'family'
        ORDER BY Timestamp DESC
        """)
    con.close()
    select = [(x[0],x[1],x[2]) for x in select]
    return render_template("room.html",messages=select)

@app.route("/logout",methods = ['GET','POST'])
def logout():
    if request.method == "POST":
        resp = make_response(render_template("message.html",message="You have been successfully logged out"))
        resp.set_cookie('Username', '', expires=0)
        return resp
    return render_template('logout.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



if __name__ == "__main__":
	from waitress import serve
	print("Serving at http://192.168.86.23:8000/ . . .")
	serve(app, host="0.0.0.0", port=8000)