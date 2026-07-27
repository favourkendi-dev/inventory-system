from marshmallow import Schema, fields, validate


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)          
    name = fields.Str(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    stock = fields.Int(required=True, validate=validate.Range(min=0))
    barcode = fields.Str(required=False, allow_none=True)


class ItemUpdateSchema(Schema):
    price = fields.Float(required=False, validate=validate.Range(min=0))
    stock = fields.Int(required=False, validate=validate.Range(min=0))