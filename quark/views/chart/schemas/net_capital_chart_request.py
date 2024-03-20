from datetime import datetime

from dateutil.relativedelta import relativedelta
from marshmallow import Schema, ValidationError, fields, post_load


class NetCapitalChartRequestSchema(Schema):
    year = fields.Str(required=True)
    start_date = fields.DateTime()
    end_date = fields.DateTime()

    @post_load
    def make_date_range(self, data, **kwargs):
        if data['year'] == 'last-year':
            data['end_date'] = datetime.now() + relativedelta(day=31)
            data['start_date'] = data['end_date'] + relativedelta(day=1, months=-11)

        else:
            try:
                data['start_date'] = datetime.strptime(data['year'], '%Y')
            except Exception as e:
                raise ValidationError('Invalid year') from e

            data['end_date'] = data['start_date'] + relativedelta(month=12, day=31)

        return data


net_capital_chart_request_schema = NetCapitalChartRequestSchema()
