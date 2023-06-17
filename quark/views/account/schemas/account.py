from marshmallow import Schema, fields


class AccountSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    is_hidden = fields.Bool()
    type = fields.Int()
    initial_balance = fields.Float()
    balance = fields.Float()


account_schema = AccountSchema()
