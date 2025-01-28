import common
import sqlite3
from sqlite3 import Connection
from flask import g


#During a request, every call to get_db() will return the same connection
#and it will be closed automatically at the end of the request.
def get_db() -> Connection:
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(common.DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception) -> None:
    db = getattr(g, '_database', None)
    if db is None:
        db.close()

def create_app(config_filename = None):
    pass

