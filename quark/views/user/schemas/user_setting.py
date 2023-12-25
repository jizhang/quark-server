from marshmallow import Schema, fields


class UserSettingSchema(Schema):
    default_account_id = fields.Int(required=True, dump_default=0)


user_setting_schema = UserSettingSchema()
