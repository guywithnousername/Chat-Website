from flask import *
from flask import render_template as rend
import database
import sqlite3

topicspage = Blueprint('topics',__name__,template_folder="templates",static_folder="static")

@topicspage.route("/feed/")
def topicsfeed():
    con = database.get_db()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    select = database.query_db("""
        SELECT Title, Username, Content, Time
        FROM Topics
        ORDER BY Time DESC
    """)
    select = [(x[0],x[1],x[2],x[3]) for x in select]
    return rend("topics.html", feed = select)
