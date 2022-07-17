import sqlite3
from database import db

class UserModel(db.Model): #THIS USERMODEL IS AN API! (exposes two endpoints find_by_id,find_by_username).it is used to interact with the user

    __tablename__ = 'users' #for accesing the table named users

    id = db.Column(db.Integer,primary_key=True)#What columns we want the table to contain
                                                #Primary key means its unique,and its going to create an index based on it
    username = db.Column(db.String(80)) #(80) limits the size of thte find_by_username
    password = db.Column(db.String(80))

    def __init__(self, username, password): #doesnt need an _id parameter,because it is already implemented above automaticallys
        self.username = username #these values must match the db.values in order to be saved to the db
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id = _id).first()
