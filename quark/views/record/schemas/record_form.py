from flask_login import current_user
from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError, \
    post_load, post_dump

from quark.models.record import RecordType
from quark.services import account as account_svc
from quark.services import record as record_svc


class RecordFormSchema(Schema):
    id = fields.Int()
    record_type = fields.Int(required=True, validate=validate.OneOf(RecordType.all()))
    category_id = fields.Int()
    account_id = fields.Int(required=True)  # TODO Validate account
    target_account_id = fields.Int()
    record_time = fields.DateTime(required=True)
    amount = fields.Decimal(required=True)
    remark = fields.Str(default='')

    @validates('id')
    def validate_id(self, value):
        if value and record_svc.get_record(current_user.id, value) is None:
            raise ValidationError('Record not found')

    @validates_schema
    def validate_category_id(self, form, **kwargs):
        if form['record_type'] not in [RecordType.EXPENSE, RecordType.INCOME]:
            return

        if not form['category_id']:
            raise ValidationError('Category cannot be empty.')

        # TODO Find category in database.

    @validates_schema
    def validate_target_account_id(self, form, **kwargs):
        if form['record_type'] != RecordType.TRANSFER:
            return

        if not form['target_account_id']:
            raise ValidationError('Target account cannot be empty.')

        if form['account_id'] == form['target_account_id']:
            raise ValidationError('Source and target account cannot be the same.')

        if account_svc.get_account(current_user.id, form['target_account_id']) is None:
            raise ValidationError('Target account not found')

    @validates_schema
    def validate_amount(self, form, **kwargs):
        if form['record_type'] == RecordType.EXPENSE and form['amount'] < 0:
            raise ValidationError('Expense amount cannot be negative.')

        if form['record_type'] == RecordType.TRANSFER and form['amount'] < 0:
            raise ValidationError('Transfer amount cannot be negative.')

    @post_load
    def load_amount(self, form, **kwargs):
        if form['record_type'] == RecordType.EXPENSE:
            form['amount'] = -form['amount']
        return form

    @post_dump
    def update_amount(self, form, **kwargs):
        if form['record_type'] == RecordType.EXPENSE:
            form['amount'] = -form['amount']
        return form


record_form_schema = RecordFormSchema()
