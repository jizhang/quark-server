from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()


def create_schema(categories: list) -> Schema:
    item_fields: dict = {'month': fields.Str()}
    for category in categories:
        item_fields[f'category_{category["id"]}'] = fields.Decimal()

    ItemSchema = Schema.from_dict(item_fields)  # noqa: N806

    ResponseSchema = Schema.from_dict({  # noqa: N806
        'categories': fields.Nested(CategorySchema, many=True),
        'data': fields.Nested(ItemSchema, many=True),
    })

    return ResponseSchema()
