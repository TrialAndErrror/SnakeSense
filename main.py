from models.processor import make_movie_review_processor
from models.api_data import YelpDataGatherer


def process_all_movies():
    # from colorama import init
    # init()
    # nlp = spacy.load('en_core_web_sm')
    # nlp.add_pipe('spacytextblob')

    processor = make_movie_review_processor()
    processor.process_reviews()
    processor.print_polar_results(3)
    processor.print_subjective_results(3)


def process_all_restaurants():
    processor = YelpDataGatherer()
    processor.create_yelp_api_obj()
    processor.search_for_restaurants()
    processor.process_all_restaurants()
    processor.get_rankings()

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
    process_all_restaurants()
