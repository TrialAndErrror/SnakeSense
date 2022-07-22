from models.processor import make_movie_review_processor
from models.api_data import YelpDataGatherer


def process_all_movies():
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


if __name__ == "__main__":
    process_all_restaurants()
