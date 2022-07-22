from yelpapi import YelpAPI
from .processor import ReviewProcessor


class Restaurant:
    yelp_obj: YelpAPI
    review_texts: list = []
    review_objs: list = []

    id: str
    name: str
    alias: str
    phone: str
    url: str
    price: str
    rating: str
    transactions: list

    processor: ReviewProcessor

    def __init__(self, yelp_obj):
        self.yelp_obj = yelp_obj

    def ingest_data(self, api_data: dict):
        self.id = api_data.get('id')
        self.name = api_data.get('name')
        self.alias = api_data.get('alias')
        self.phone = api_data.get('phone')
        self.url = api_data.get('url')
        self.price = api_data.get('price')
        self.rating = api_data.get('rating')
        self.transactions = api_data.get('transactions')

    def get_reviews(self):
        self.review_texts = self.yelp_obj.reviews_query(
            id=self.id
        )

        saved_keys = ['id', 'rating', 'text', 'url']

        for item in self.review_texts['reviews']:
            data = {
                key: item.get(key)
                for key in saved_keys
            }
            if item.get('user'):
                data['name'] = item['user'].get('name', 'Anonymous User')
            else:
                data['name'] = 'Anonymous User'

        self.review_objs = [{
            key: item.get(key)
            for key in saved_keys
        } for item in self.review_texts['reviews']]

    def process_reviews(self):
        reviews_list = [(item.get('name'), item.get('text'))
                        for item in self.review_objs]
        self.processor = ReviewProcessor(reviews_list)
        self.processor.process_reviews()

    def print_results(self):
        print(f'\nResults for {self.name}')
        print(f'* Rating: {self.rating}')
        print(f'* Price: {self.price}\n')

        print('\n****** Sorted by Polarity: ******\n')
        results = self.processor.get_polar_results()
        for review in results:
            print(f"User Name: {review.file_name}")
            review.print_subjectivity()
            review.print_polarity()
            print(f"{review.text}")

        print('\n****** Sorted by Subjectivity: ******\n')
        results = self.processor.get_subjective_results()
        for review in results:
            print(f"User Name: {review.file_name}")
            review.print_subjectivity()
            review.print_polarity()
            print(f"{review.text}")

    def get_results(self):
        return {
            'name': self.name,
            'rating': self.rating,
            'price': self.price,
            'polar': self.processor.get_polar_results(),
            'subjective': self.processor.get_subjective_results(),
            "score": self.get_score()
        }

    def get_score(self):
        review_scores = [review.get_score()
                         for review in self.processor.results]
        return sum(review_scores) / len(review_scores)
