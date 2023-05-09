from quark import db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    record_type = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    account_id = db.Column(db.Integer)
    target_account_id = db.Column(db.Integer)
    record_time = db.Column(db.DateTime)
    amount = db.Column(db.Numeric)
    remark = db.Column(db.String)
    is_deleted = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


class RecordType:
    EXPENSE = 1
    INCOME = 2
    TRANSFER = 3

    @classmethod
    def all(cls):
        return [cls.EXPENSE, cls.INCOME, cls.TRANSFER]
