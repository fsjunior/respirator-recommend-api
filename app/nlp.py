import spacy

from app.common import settings

nlp = spacy.load(settings.nlp_model_path)
