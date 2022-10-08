from flask import *
from flask import render_template as rend
import database
import sqlite3
from datetime import datetime

topicspage = Blueprint('topics',__name__,template_folder="templates",static_folder="static")

@topicspage.route("/feed/")
def topicsfeed():
    con = database.get_db()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    select = database.query_db("""
        SELECT Title, Username, Content, Time
        FROM Topics
        ORDER BY Acttime DESC
    """)
    select = [(x[0],x[1],x[2],x[3]) for x in select]
    return rend("topics.html", feed = select)

@topicspage.route("/post/", methods = ['GET', 'POST'])
def newpost():
    con = database.get_db()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    name = request.cookies.get("Username")
    if not name:
        return rend("message.html",message="You aren't logged in.")
    
    if (request.method == "POST"):
        time = datetime.now().strftime("%B %d, %Y %I:%M%p")
        acttime = int(datetime.now().strftime("%s"))
        title = request.form.get("title")
        content = request.form.get("content")
        cur.execute("""
        INSERT INTO Topics (Title, Username, Content, Time, Acttime)
        VALUES (?,?,?,?,?)
        """, (title, name, content, time, acttime))
        con.commit()
        return rend("message.html",message="Posted!")
    con.close()
    return rend("newpost.html")
