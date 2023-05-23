from marshmallow import Schema, fields, validate


class CategoryChartRequestSchema(Schema):
    type = fields.Str()
    month = fields.DateTime(required=True, format='%Y%m')


category_chart_request_schema = CategoryChartRequestSchema()
