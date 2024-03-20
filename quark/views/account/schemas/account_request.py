from flask_login import current_user
from marshmallow import Schema, ValidationError, fields, post_load

from quark.services import account as account_svc


class AccountRequestSchema(Schema):
    id = fields.Int(required=True)

    @post_load
    def make_account(self, data, **kwargs):
        account = account_svc.get_account(current_user.id, data['id'])
        if account is None:
            raise ValidationError('Account not found')
        return account


account_request_schema = AccountRequestSchema()
