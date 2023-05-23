from marshmallow import Schema, fields, validate


class CategoryChartRequestSchema(Schema):
    type = fields.Int(required=True, validate=validate.OneOf([1, 2]))
    month = fields.DateTime(required=True, format='%Y%m')


category_chart_request_schema = CategoryChartRequestSchema()
