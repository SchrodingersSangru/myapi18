import sqlite3


def insertUser(username, password):
    con = sqlite3.connect("first.db")
    cur = con.cursor()
    table = """CREATE TABLE TaskEntry(username VARCHAR(255), password VARCHAR(255), task VARCHAR(255));"""
    cur.execute(table)
    con.commit()
    con.close()


def retrieveUsersAdmin():
    con = sqlite3.connect("first.db")
    cur = con.cursor()
    query = """SELECT username, task FROM TaskEntry"""
    data = cur.execute(query)
    con.close()
    return data

def retrieveUser():
    con = sqlite3.connect("first.db")
    cur = con.cursor()
    cur.execute("SELECT username, task from users1 where ")
    users = cur.fetchall()
    con.close()
    return users
