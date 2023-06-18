from flask_login import current_user
from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError

from quark.models.account import AccountType
from quark.services import account as account_svc


class AccountSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(min=1))
    is_hidden = fields.Bool(load_default=False)
    type = fields.Int(required=True, validate=validate.OneOf(AccountType.all()))
    initial_balance = fields.Decimal(required=True)
    balance = fields.Decimal()

    @validates('id')
    def validate_id(self, value):
        if value and account_svc.get_account(current_user.id, value) is None:
            raise ValidationError('Account not found')

    @validates_schema
    def validate_name(self, form, **kwargs):
        by_name = account_svc.get_account_by_name(current_user.id, form['name'])
        if by_name is not None and ('id' not in form or by_name.id != form['id']):
            raise ValidationError('Account name is duplicate.')


account_schema = AccountSchema()
