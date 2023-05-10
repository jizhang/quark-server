from marshmallow import Schema, fields


class RecordItemSchema(Schema):
    id = fields.Int()
    record_type = fields.Int()
    category_name = fields.Str()
    account_name = fields.Str()
    target_account_name = fields.Str()
    record_time = fields.DateTime()
    amount = fields.Decimal()
    remark = fields.Str()


record_item_schema = RecordItemSchema()
