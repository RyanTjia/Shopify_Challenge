import sys
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import *

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/list_item", methods = ["GET"])
def list_item():
	items = Item.query.all()
	return render_template("AddItem.html", items = items)

@app.route("/add_item", methods = ["POST"])
def add_item():
	name = request.form.get("name")
	category = request.form.get("category")
	description = request.form.get("description")
	price = request.form.get("price")

	item = Item(name = name, category = category, description = description, price = price)
	db.session.add(item)
	db.session.commit()

	items = Item.query.all()
	return render_template("AddItem.html", items = items)

@app.route("/edit_item/<int:item_id>", methods = ["GET", "POST"])
def edit_item(item_id):
	item = Item.query.get(item_id)

	if request.method == 'POST':
		item.name = request.form.get("name")
		item.category = request.form.get("category")
		item.description = request.form.get("description")
		item.price = request.form.get("price")

		db.session.commit()

	return render_template("EditItem.html", item = item)

@app.route("/delete_item/<int:item_id>", methods = ["GET"])
def delete_item(item_id):
	item = Item.query.get(item_id)
	ItemsToWarehouse.query.filter_by(item_id = item_id).delete()
	db.session.delete(item)
	db.session.commit()

	items = Item.query.all()
	return render_template("AddItem.html", items = items)

@app.route("/list_warehouse", methods = ["GET"])
def list_warehouse():
	warehouses = Warehouse.query.all()
	return render_template("AddWarehouse.html", warehouses = warehouses)

@app.route("/add_warehouse", methods = ["POST"])
def add_warehouse():
	address = request.form.get("address")
	state = request.form.get("state")
	zipcode = str(request.form.get("zipcode"))

	warehouse = Warehouse(address = address, state = state, zipcode = zipcode)
	db.session.add(warehouse)
	db.session.commit()

	warehouses = Warehouse.query.all()
	return render_template("AddWarehouse.html", warehouses = warehouses)

@app.route("/edit_warehouse/<int:warehouse_id>", methods = ["GET", "POST"])
def edit_warehouse(warehouse_id):
	warehouse = Warehouse.query.get(warehouse_id)

	if request.method == 'POST':
		warehouse.address = request.form.get("address")
		warehouse.state = request.form.get("state")
		warehouse.zipcode = str(request.form.get("zipcode"))

		db.session.commit()

	return render_template("EditWarehouse.html", warehouse = warehouse)

@app.route("/delete_warehouse/<int:warehouse_id>", methods = ["GET"])
def delete_warehouse(warehouse_id):
	warehouse = Warehouse.query.get(warehouse_id)
	ItemsToWarehouse.query.filter_by(warehouse_id = warehouse_id).delete()
	db.session.delete(warehouse)
	db.session.commit()
	
	warehouses = Warehouse.query.all()
	return render_template("AddWarehouse.html", warehouses = warehouses)

@app.route("/store_item/<int:choice>/<int:id>", methods = ["POST"])
def store_item(choice, id):

	targetID = request.form.get("targetID")
	stock = request.form.get("stock")

	#If choice is 1 then the warehouse is linked to the item
	if choice == 1:
		item = Item.query.get(id)

		if Warehouse.query.get(targetID) is not None:

			if ItemsToWarehouse.query.filter_by(item_id = id, warehouse_id = targetID).first() is not None:
				Storage = ItemsToWarehouse.query.filter_by(item_id = id, warehouse_id = targetID).first()
				Storage.stock = stock
			else:
				action = ItemsToWarehouse(item_id = id, warehouse_id = targetID, stock = stock)
				db.session.add(action)
			db.session.commit()

		return render_template("EditItem.html", item = item)

	#Else if choice is 2 then the item is linked to the warehouse
	elif choice == 2:
		warehouse = Warehouse.query.get(id)

		if Item.query.get(targetID) is not None:

			if ItemsToWarehouse.query.filter_by(item_id = targetID, warehouse_id = id).first() is not None:
				Storage = ItemsToWarehouse.query.filter_by(item_id = targetID, warehouse_id = id).first()
				Storage.stock = stock
			else:
				action = ItemsToWarehouse(item_id = targetID, warehouse_id = id, stock = stock)
				db.session.add(action)
			db.session.commit()

		return render_template("EditWarehouse.html", warehouse = warehouse)

def main():
	if (len(sys.argv) == 2):
		print(sys.argv)
		if sys.argv[1] == 'createdb':            
			db.create_all()
	else:
		print("Run app using 'flask run'")
		print("To create a database use 'python app.py createdb")

# Run the main method in the context of our flass application
# This allows db know about our models.
if __name__ == "__main__":
	with app.app_context():        
		main()