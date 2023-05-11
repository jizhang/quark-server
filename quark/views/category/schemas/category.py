from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Int()
    type = fields.Int()
    name = fields.Str()


category_schema = CategorySchema()
