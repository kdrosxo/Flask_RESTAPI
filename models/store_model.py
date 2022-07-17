from database import db

class StoreModel(db.Model): #Tells the SQLAlchemy that the ItemModel will be saved in a db

    __tablename__ = 'stores'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    #SQLALCHEMY will read the above variables and insert them in the init method below

    items = db.relationship('ItemModel', lazy = 'dynamic') #it allows the store to find which items are in the items table, with a store_id equal to its own id.
                                         #the above variable is a list of item models bcs it know it is a 1-N relationship.
                                         #lazy = dynamic tells the StoreModel to NOT retrieve associated items from the items table at the time of its creation

    def __init__(self,name):
        self.name = name


    def json(self):
        return {'name':self.name,'items':[item.json() for item in self.items.all()]} #SInce StoreModel doesnt have associated items loaded,we cannon use self.ItemList
                                                                                    #Insted we have to use self.items.all(), A QUERY,to load all items.

    @classmethod
    def find_by_name(cls,name): #Instead of ItemModel we can use cls. this method returns and ItemModel object that has self.name self.price
        return cls.query.filter_by(name=name).first()#SELECT * FROM items(__tablename__) WHERE name=name(which we pass with the method) LIMIT 1


    def save_to_db(self): #when we change the name of the object and add it to the session again, the SQLALCHEMY know and updates it via this method,so its both update/insert
        db.session.add(self) #The session in this instance is a collection of objects that we're going to write in the database.
        db.session.commit()



    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
