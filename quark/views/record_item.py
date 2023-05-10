from marshmallow import Schema, fields


class RecordItemSchema(Schema):
    id = fields.Int()
    record_type = fields.Int()
    category_name = fields.Method('get_category_name')
    account_name = fields.Method('get_account_name')
    target_account_name = fields.Method('get_target_account_name')
    record_time = fields.DateTime()
    amount = fields.Decimal()
    remark = fields.Str()

    def get_category_name(self, record):
        return self.context['category_names'].get(record.category_id)

    def get_account_name(self, record):
        return self.context['account_names'].get(record.account_id)

    def get_target_account_name(self, record):
        return self.context['account_names'].get(record.target_account_id)
