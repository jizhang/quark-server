from flask_login import current_user
from marshmallow import Schema, ValidationError, fields, post_load

from quark.services import record as record_svc


class RecordRequestSchema(Schema):
    id = fields.Int(required=True)

    @post_load
    def make_record(self, data, **kwargs):
        row = record_svc.get_record(current_user.id, data['id'])
        if row is None:
            raise ValidationError('Record not found')
        return row


record_request_schema = RecordRequestSchema()
