from flask_login import current_user
from marshmallow import Schema, fields, validates, ValidationError

from quark.services import account as account_svc


class AccountMoveSchema(Schema):
    active_id = fields.Int(required=True)
    over_id = fields.Int(required=True)

    @validates('active_id')
    def validate_active_id(self, value: int):
        if account_svc.get_account(current_user.id, value) is None:
            raise ValidationError('Active account ID not found')

    @validates('over_id')
    def validate_over_id(self, value: int):
        if account_svc.get_account(current_user.id, value) is None:
            raise ValidationError('Over account ID not found')


account_move_schema = AccountMoveSchema()
