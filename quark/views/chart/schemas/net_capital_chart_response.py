from marshmallow import Schema, fields


class ChartItemSchema(Schema):
    month = fields.Str()
    amount = fields.Decimal()


class NetCapitalChartResponseSchema(Schema):
    data = fields.Nested(ChartItemSchema, many=True)


net_capital_chart_response_schema = NetCapitalChartResponseSchema()
