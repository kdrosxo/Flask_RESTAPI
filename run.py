from app import app
from db import db
db.init_app(app)


@app.before_first_request #this is a decorator that will affect the method below it ,and its going to run that method before the first request in this init_app
def create_tables():
    db.create_all() 
