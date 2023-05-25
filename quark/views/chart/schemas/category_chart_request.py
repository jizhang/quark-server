from dateutil.relativedelta import relativedelta
from marshmallow import Schema, fields, post_load


class CategoryChartRequestSchema(Schema):
    month = fields.DateTime(required=True, format='%Y%m')
    start_date = fields.DateTime()
    end_date = fields.DateTime()

    @post_load
    def make_date_range(self, data, **kwargs):
        data['start_date'] = data['month']
        data['end_date'] = data['month'] + relativedelta(day=31)
        return data


category_chart_request_schema = CategoryChartRequestSchema()
