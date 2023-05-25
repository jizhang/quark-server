from marshmallow import Schema, fields, validate

from quark.models.record import RecordType


class RecordListRequestSchema(Schema):
    record_type = fields.Int(validate=validate.OneOf(RecordType.all()))
    account_id = fields.Int()
    last_id = fields.Int(load_default=0)
    limit = fields.Int(load_default=10_000)


record_list_request_schema = RecordListRequestSchema()
