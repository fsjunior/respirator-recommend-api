from marshmallow import EXCLUDE, Schema, fields, validate


class ApprovalCertificateSchema(Schema):
    number = fields.Int(description="Number")
    manufacturer = fields.String(description="Manufacturer Name")
    valid = fields.Bool(description="AC Validity")


class RespiratorSchema(Schema):
    id = fields.String(dump_only=True, description="Respirator Entry ID")
    url = fields.String(required=True, description="Respirator Site URL")
    respirator_type = fields.Str(
        required=False, validate=validate.OneOf(["PFF1", "PFF2", "PFF3", "KN95"]), description="Type of the respirator"
    )
    exhalation_valve = fields.Bool(required=False, description="Exhalation Valve")
    approval_certificate = fields.Nested('ApprovalCertificateSchema', description="Approval Certificate Info")
    spandex = fields.Bool(required=False, description="This respirator uses spandex?")
    quantity = fields.Int(required=True, description="Offer quantity")
    price_per_unit = fields.Float(required=False, description="Price tag per unit")

    class Meta:
        restrict = True


class RespiratorQueryArgsSchema(Schema):
    url = fields.URL(required=False, description="Respirator Site URL")

    class Meta:
        # This is needed otherwise the schema validation will
        # fail with the pagination parameters
        unknown = EXCLUDE
