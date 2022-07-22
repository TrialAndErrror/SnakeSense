from pip import main
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from pathlib import Path


UNSUP_TRAIN_DIRECTORY = Path('./aclImdb/train/unsup')
NEG_TRAIN_DIRECTORY = Path('./aclImdb/train/neg')
POS_TRAIN_DIRECTORY = Path('./aclImdb/train/pos')


def get_sentiment(doc):
    return doc._.blob.sentiment


def process_all():

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')

    reviews = UNSUP_TRAIN_DIRECTORY.glob('*.txt')

    results = {}
    review_count = 3
    for num in range(review_count):
        review = next(reviews)
        with open(Path(review), 'r') as file:
            text = file.read()

        # read file
        doc = nlp(text)
        sentiment = get_sentiment(doc)

        results[review.name] = {
            "text": text,
            "subjectivity": sentiment.subjectivity,
            "polarity": sentiment.polarity
        }

    print(results)


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

if __name__ == "__main__":
    process_all()