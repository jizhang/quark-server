from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    amount = fields.Decimal()
    percent = fields.Float()


class GroupSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    amount = fields.Decimal()
    categories = fields.Nested(CategorySchema, many=True)


class CategoryChartResponseSchema(Schema):
    groups = fields.Nested(GroupSchema, many=True)


category_chart_response_schema = CategoryChartResponseSchema()
