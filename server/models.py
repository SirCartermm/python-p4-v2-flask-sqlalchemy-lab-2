from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy_serializer import SerializerMixin   # type: ignore

db = SQLAlchemy()  
class Customer(db.Model, SerializerMixin):  
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  

    reviews = db.relationship('Review', back_populates='customer', overlaps="items")  
    items = db.relationship('Item', secondary='reviews', primaryjoin='Customer.id==Review.customer_id', secondaryjoin='Review.item_id==Item.id', lazy='dynamic', overlaps="reviews")  

class Item(db.Model, SerializerMixin):  
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  

    reviews = db.relationship('Review', back_populates='item', overlaps="customer_reviews")  
    customer_reviews = db.relationship('Review', back_populates='item', lazy='dynamic', overlaps="reviews")  

class Review(db.Model, SerializerMixin):  
    id = db.Column(db.Integer, primary_key=True)  
    review = db.Column(db.String(255), nullable=False)  

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)  
    customer = db.relationship('Customer', back_populates='reviews', overlaps="items")  

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)  
    item = db.relationship('Item', back_populates='reviews', overlaps="customer_reviews")  