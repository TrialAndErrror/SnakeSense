import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from pathlib import Path


UNSUP_TRAIN_DIRECTORY = Path('./aclImdb/train/unsup')
NEG_TRAIN_DIRECTORY = Path('./aclImdb/train/neg')
POS_TRAIN_DIRECTORY = Path('./aclImdb/train/pos')


def make_doc_object(text):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')
    doc = nlp(text)
    return doc


def get_sentiment(blob):
    return blob.sentiment

def process_all():
    reviews = []

    results = {}
    for review in reviews:
        with open(Path(review), 'r') as file:
            text = file.read()

        # read file
        doc = make_doc_object(review)
        sentiment = get_sentiment(doc._.blob)

        results[review] = {
            "text": text,
            "subjectivity": sentiment.subjectivity,
            "polarity": sentiment.polarity

        }




"""
Polarity: {doc._.blob.polarity}
Subjectivity: {doc._.blob.subjectivity}
Assessments: {doc._.blob.sentiment_assessments.assessments}
NGrams: {doc._.blob.ngrams()}
"""

"""
doc._.blob.sentiment
Polarity measures whether the expressed opinion is positive (1.0), negative (-1.0), or neutral.
Subjectivity measures how objective (0.0) or subjective (1.0) a statement is.

doc._.blob.words
doc._.blob.words[index].singularize()
doc._.blob.words[index].pluralize()
"""
