from datetime import datetime

from marshmallow import Schema, fields, validate

from quark.models.record import RecordType


class RecordListRequestSchema(Schema):
    record_type = fields.Int(validate=validate.OneOf(RecordType.all()))
    category_id = fields.Int()
    account_id = fields.Int()
    keyword = fields.Str()
    year = fields.DateTime('%Y', load_default=lambda: datetime.now())


record_list_request_schema = RecordListRequestSchema()
