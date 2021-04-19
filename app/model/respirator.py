import datetime

from flask_mongoengine import Document
from mongoengine import CASCADE, BooleanField, DateTimeField, FloatField, IntField, ReferenceField, StringField


class ApprovalCertificate(Document):
    date = DateTimeField(required=True, default=datetime.datetime.now)
    number = IntField(required=True)
    manufacturer = StringField(required=False)
    ac_class = StringField(required=False)
    valid = BooleanField(required=False)
    good_ac = BooleanField(required=True, default=False)


class Respirator(Document):
    url = StringField(required=True)
    title = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now)
    respirator_type = StringField(required=False)
    exhalation_valve = BooleanField(required=False)
    approval_certificate = ReferenceField("ApprovalCertificate", reverse_delete_rule=CASCADE)
    spandex = BooleanField(required=False)
    quantity = IntField(required=False)
    price_per_unit = FloatField(required=False)

    def __repr__(self):
        return f"{self.approval_certificate.number} - {self.approval_certificate.manufacturer}"
