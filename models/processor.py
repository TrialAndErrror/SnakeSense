import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from .review import Review
from typing import List, Text, Tuple
from pathlib import Path

UNSUP_TRAIN_DIRECTORY = Path('./aclImdb/train/unsup')
NEG_TRAIN_DIRECTORY = Path('./aclImdb/train/neg')
POS_TRAIN_DIRECTORY = Path('./aclImdb/train/pos')


class ReviewProcessor:
    reviews: List[Tuple[Text, Text]] = []
    results: List[Review] = []

    def __init__(self, reviews: list):
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe('spacytextblob')

        self.reviews = reviews

    def process_reviews(self):
        self.results = [self.process_one_review(filename, text) for filename, text in self.reviews]

    def process_one_review(self, filename, text):
        sentiment = self.nlp(text)._.blob.sentiment
        return Review(
                name=filename,
                text=text,
                subjectivity=sentiment.subjectivity,
                polarity=sentiment.polarity,
            )

    def get_polar_results(self):
        self.results.sort(key=lambda x: x.polarity, reverse=True)
        return self.results

    def print_polar_results(self, num_results: int):
        print()
        results = self.get_polar_results()
        print_section_header("Positive Reviews")
        [review.print() for review in results[:num_results]]
        print('\n\n')
        print_section_header("Negative Reviews")
        [review.print() for review in results[-num_results:]]
        print()

    def get_subjective_results(self):
        self.results.sort(key=lambda x: x.subjectivity, reverse=True)
        return self.results

    def print_subjective_results(self, num_results: int):
        print()
        results = self.get_subjective_results()
        print_section_header('Most Subjective Reviews')
        [review.print() for review in results[:num_results]]
        print('\n\n')
        print_section_header('Least Subjective Reviews')
        [review.print() for review in results[-num_results:]]
        print()


def make_movie_review_processor():
    def get_one_file_text(review_file):
        with open(review_file, 'r') as file:
            text = file.read()
        return review_file.name, text

    review_count: int = 100
    review_files = UNSUP_TRAIN_DIRECTORY.glob('*.txt')

    texts_to_review = []
    for _ in range(review_count):
        review_file = next(review_files)
        review_filename, text = get_one_file_text(review_file)
        texts_to_review.append((review_filename, text))

    obj = ReviewProcessor(texts_to_review)

    return obj


def print_section_header(text):
    print("*" * 10 + f" {text} " + "*" * 10)
