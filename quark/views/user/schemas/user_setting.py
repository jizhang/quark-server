from marshmallow import Schema, fields


class UserSettingSchema(Schema):
    default_account_id = fields.Int(required=True)


user_setting_schema = UserSettingSchema()
