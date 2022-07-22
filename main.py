from pip import main
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from pathlib import Path
from models.processor import ReviewProcessor


UNSUP_TRAIN_DIRECTORY = Path('./aclImdb/train/unsup')
NEG_TRAIN_DIRECTORY = Path('./aclImdb/train/neg')
POS_TRAIN_DIRECTORY = Path('./aclImdb/train/pos')


def get_sentiment(doc):
    return doc._.blob.sentiment


def process_all():
    from colorama import init
    init()
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')

    review_files = UNSUP_TRAIN_DIRECTORY.glob('*.txt')

    processor = ReviewProcessor(review_files)
    processor.process_reviews()
    processor.print_polar_results(3)
    processor.print_subjective_results(3)


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