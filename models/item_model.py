from database import db

class ItemModel(db.Model): #Tells the SQLAlchemy that the ItemModel will be saved in a db

    __tablename__ = 'items'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    #SQLALCHEMY will read the above variables and insert them in the init method below
    store_id=db.Column(db.Integer,db.ForeignKey('stores.id')) #foreign key links e.g store with id=2 with the items with id=2, and SQL dbs wont let you delete the store table
    store = db.relationship('StoreModel') #now every item model has a property Store that is the store which matches the store_id in its id.

    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name,'price':self.price}

    @classmethod
    def find_by_name(cls,name): #Instead of ItemModel we can use cls. this method returns and ItemModel object that has self.name self.price
        return cls.query.filter_by(name=name).first()#SELECT * FROM items(__tablename__) WHERE name=name(which we pass with the method) LIMIT 1


    def save_to_db(self): #when we change the name of the object and add it to the session again, the SQLALCHEMY know and updates it via this method,so its both update/insert
        db.session.add(self) #The session in this instance is a collection of objects that we're going to write in the database.
        db.session.commit()



    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
