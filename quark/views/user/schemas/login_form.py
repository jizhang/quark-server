from marshmallow import Schema, fields, validate


class LoginFormSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=1))
    remember_me = fields.Str(load_default='1')


login_form_schema = LoginFormSchema()
