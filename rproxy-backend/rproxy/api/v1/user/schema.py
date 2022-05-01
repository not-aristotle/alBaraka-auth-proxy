from marshmallow import Schema, fields, validate


class AuthSchema(Schema):
    code = fields.Str(validate=[validate.Length(max=1024)], required=True)
    redirect_uri = fields.Str(validate=[validate.Length(max=1024)], required=True)
