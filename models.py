from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#Many-to-many relationship
class ItemsToWarehouse(db.Model):
	__tablename__ = "stored"
	
	item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable = False, primary_key = True)
	warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable = False, primary_key = True)
	stock = db.Column(db.Integer, default = 0)

	item = db.relationship("Item", backref = "stored", lazy = True)
	warehouse = db.relationship("Warehouse", backref = "stored", lazy = True)

#Create inventory item
class Item(db.Model):
	__tablename__ = "items"

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, nullable = False)
	category = db.Column(db.String, nullable = False)
	description = db.Column(db.String, nullable = False)
	price = db.Column(db.Numeric(10, 2), nullable = False)

	warehouses = db.relationship("Warehouse", secondary = "stored")

#Create warehouses
class Warehouse(db.Model):
	__tablename__ = "warehouses"

	id = db.Column(db.Integer, primary_key = True)
	address = db.Column(db.String, nullable = False)
	state = db.Column(db.String, nullable = False)
	zipcode = db.Column(db.String, nullable = False)

	items = db.relationship("Item", secondary = "stored")