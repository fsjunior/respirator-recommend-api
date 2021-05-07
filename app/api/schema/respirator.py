from marshmallow import EXCLUDE, Schema, fields, validate


class ApprovalCertificateSchema(Schema):
    number = fields.Int(metadata={"description": "Number"})
    manufacturer = fields.String(metadata={"description": "Manufacturer Name"})
    valid = fields.Bool(metadata={"description": "AC Validity"})


class RespiratorSchema(Schema):
    id = fields.String(dump_only=True, metadata={"description": "Respirator Entry ID"})
    title = fields.String(required=True, metadata={"description": "Respirator Site Title"})
    date = fields.DateTime(metadata={"description": "Last time updated"})
    url = fields.String(required=True, metadata={"description": "Respirator Site URL"})
    respirator_type = fields.Str(
        required=False,
        validate=validate.OneOf(["PFF1", "PFF2", "PFF3", "KN95"]),
        metadata={"description": "Type of the respirator"},
    )
    exhalation_valve = fields.Bool(required=False, metadata={"description": "Exhalation Valve"})
    approval_certificate = fields.Nested(
        ApprovalCertificateSchema, metadata={"description": "Approval Certificate Info"}
    )
    spandex = fields.Bool(required=False, metadata={"description": "This respirator uses spandex?"})
    quantity = fields.Int(required=True, metadata={"description": "Offer quantity"})
    price_per_unit = fields.Float(required=False, metadata={"description": "Price tag per unit"})

    class Meta:
        restrict = True


class RespiratorQueryArgsSchema(Schema):
    url = fields.URL(required=False, metadata={"description": "Respirator Site URL"})

    class Meta:
        # This is needed otherwise the schema validation will
        # fail with the pagination parameters
        unknown = EXCLUDE
