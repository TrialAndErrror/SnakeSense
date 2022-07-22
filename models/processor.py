from ctypes import pointer
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from .review import Review
from typing import List, Text


class ReviewProcessor:
    review_files: List[Text] = []
    results: List[Review] = []
    review_count: int = 100

    def __init__(self, review_files):
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe('spacytextblob')

        self.review_files = review_files

    def process_reviews(self):
        for _ in range(self.review_count):

            review_filename, text = self.get_next_review_text()
            doc = self.nlp(text)

            sentiment = self.get_sentiment(doc)

            self.results.append(Review(
                file_name=review_filename,
                text=text,
                subjectivity=sentiment.subjectivity,
                polarity=sentiment.polarity,
            ))

    def get_next_review_text(self):
        review_file = next(self.review_files)
        with open(review_file, 'r') as file:
            text = file.read()
        return review_file.name, text

    def get_sentiment(self, doc):
        return doc._.blob.sentiment

    def print_polar_results(self, num_results: int):
        print()
        self.results.sort(key=lambda x: x.polarity, reverse=True)
        print_section_header("Positive Reviews")
        [review.print() for review in self.results[:num_results]]
        print('\n\n')
        print_section_header("Negative Reviews")
        [review.print() for review in self.results[-num_results:]]
        print()

    def print_subjective_results(self, num_results: int):
        print()
        self.results.sort(key=lambda x: x.subjectivity, reverse=True)
        print_section_header('Most Subjective Reviews')
        [review.print() for review in self.results[:num_results]]
        print('\n\n')
        print_section_header('Least Subjective Reviews')
        [review.print() for review in self.results[-num_results:]]
        print()


def print_section_header(text):
    print("*" * 10 + f" {text} " + "*" * 10) 