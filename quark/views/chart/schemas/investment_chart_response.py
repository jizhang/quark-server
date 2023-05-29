from marshmallow import Schema, fields


class AccountSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    amount = fields.Decimal()
    percent = fields.Float()


class InvestmentChartResponseSchema(Schema):
    record_type = fields.Int()
    category_id = fields.Int()
    total = fields.Decimal()
    accounts = fields.Nested(AccountSchema, many=True)


investment_chart_response_schema = InvestmentChartResponseSchema()
