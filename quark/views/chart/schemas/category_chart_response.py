from marshmallow import Schema, fields


class ChartItemSchema(Schema):
    category_id = fields.Int()
    category_name = fields.Str()
    amount = fields.Decimal()
    percent = fields.Float()


class CategoryChartResponseSchema(Schema):
    data = fields.Nested(ChartItemSchema, many=True)


category_chart_response_schema = CategoryChartResponseSchema()
