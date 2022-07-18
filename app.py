import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item , ItemList
from resources.store import Store , StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE'),'sqlite:///data.db') #To tell the SQLALCHEMY where to find the data.db ,is goind to read the file.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #as to not consume Resources tracking modifications and changes
app.secret_key = 'drosxo'
api = Api(app)

#@app.before_first_request #this is a decorator that will affect the method below it ,and its going to run that method before the first request in this init_app
#def create_tables():
#    db.create_all() #SQLALCHEMY sees the models we imported in the main app, so for anything that subclasses db.Model ,it will create tables with the columns defined in the class

jwt = JWT(app,authenticate,identity) # /auth

api.add_resource(Store,'/store<string:name>')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run(port=5000, debug = True)
