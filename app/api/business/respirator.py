from typing import List, Type

from app.api.business.common import find_by_id
from app.api.exceptions.respirator import RespiratorNotFound
from app.model.respirator import Respirator
from app.nlp import nlp


def find_respirator_by_id(doc_class: Type[Respirator], doc_id: str) -> Respirator:
    return find_by_id(doc_class, doc_id, RespiratorNotFound)


def find_first(values: List[str], dictionary: dict):
    for value in values:
        if value in dictionary:
            return value
    return None


def analyze_website(url: str) -> Respirator:
    text = nlp(url.lower())

    respirator = Respirator(url=url)

    detected_labels = {entity.label_: entity.text for entity in text.ents}

    respirator_type = find_first(["KN95", "PFF3", "PFF2", "PFF1"], detected_labels)
    if respirator_type is not None:
        respirator.respirator_type = respirator_type

    exhalation_valve = find_first(["CV", "SV"], detected_labels)
    if exhalation_valve is not None:
        respirator.exhalation_valve = exhalation_valve == "CV"

    if "EL" in detected_labels:
        respirator.spandex = True

    if "QT" in detected_labels:
        try:
            respirator.quantity = int(detected_labels["QT"])
        except ValueError:
            respirator.quantity = 1
    else:
        respirator.quantity = 1

    if "CA" in detected_labels:
        try:
            respirator.certification = int(detected_labels["CA"])
        except ValueError:
            pass

    return respirator
