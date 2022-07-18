import os
import sqlite3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
        SQLALCHEMY_DATABASE_URI = "users.sqlite3"
    )
    
    # Init Database
    db = SQLAlchemy(app)
    
    # Create table in database
    class Users(db.Model):
        id = db.Column("student_id", db.Integer, primary_key=True)
        username = db.Column("username", db.String(50))
        password = db.Column("password", db.String(50))
        email = db.Column("email", db.String(50))

        def __init__(self, username, password, email) -> None:
            self.username = username
            self.password = password
            self.email = email
            
    db.create_all()
    
    return app, Users
    
    