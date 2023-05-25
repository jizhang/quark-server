from marshmallow import Schema, fields


class AccountSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    amount = fields.Decimal()
    percent = fields.Float()


class InvestmentChartResponseSchema(Schema):
    total = fields.Decimal()
    accounts = fields.Nested(AccountSchema, many=True)


investment_chart_response_schema = InvestmentChartResponseSchema()
