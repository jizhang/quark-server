from quark import db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String)
    type = db.Column(db.Integer)
    initial_balance = db.Column(db.Numeric)
    balance = db.Column(db.Numeric)
    order_num = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
