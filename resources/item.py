from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('price',type=float,required = True,
    help = "This field cannot be blank")

    parser.add_argument('store_id',type=int,required = True,
    help = "Every item needs a store ID")

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"item not found"},404


    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message":"An item with name '{}'already exists".format(name)},400

        request_data = Item.parser.parse_args()

        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except Exception as e:
            print(e)
            return{"message":"An error occured inserting the item"},500

        return item.json(), 201


    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': "Item deleted"}

    def put(self,name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name,**request_data) #If the search doesn find the item with the specific name it will create it
        else:
            item.price = request_data['price'] #If there is an item with the specific name it will just update the price

        item.save_to_db()

        return item.json()



class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
