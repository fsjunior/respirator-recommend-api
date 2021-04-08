from flask_mongoengine import Document
from mongoengine import BooleanField, FloatField, IntField, StringField


class Respirator(Document):
    url = StringField(required=True)
    respirator_type = StringField(required=False)
    exhalation_valve = BooleanField(required=False)
    certification = IntField(required=False)
    spandex = BooleanField(required=False)
    quantity = IntField(required=True)
    price_per_unit = FloatField(required=False)
