import json
from yelpapi import YelpAPI
from typing import List, Dict, Text
from .restaurant import Restaurant
from pprint import pprint


class YelpDataGatherer:
    yelp_obj: YelpAPI
    restaurants: list = []
    business_list: list = []

    def __init__(self):
        self.create_yelp_api_obj()

    def create_yelp_api_obj(self):
        with open('./models/api_config.json', 'r') as file:
            api_key = json.load(file).get('API_KEY')

        self.yelp_obj = YelpAPI(api_key, timeout_s=3.0)

    def search_for_restaurants(self):
        """
        Get all restaurants that mention that they serve fried chicken.
        """
        print('Searching for Restaurants...')
        results = self.yelp_obj.search_query(
            term="\"fried chicken\"",
            location="arkansas",
            category="bbq,chicken_shop,chinese,chicken_wings,soulfood",
            limit=50
        )

        self.business_list = results['businesses']

    def process_all_restaurants(self, debug=False):
        print('Processing Restaurants...')
        for item in self.business_list:
            new_restaurant = Restaurant(self.yelp_obj)
            new_restaurant.ingest_data(item)
            print(f'Processing {new_restaurant.name}')
            self.restaurants.append(new_restaurant)
            new_restaurant.get_reviews()
            new_restaurant.process_reviews()

    def get_rankings(self):
        print('Calculating Rankings')
        overall_rankings = [
            item.get_results() for item in self.restaurants]
        overall_rankings.sort(key=lambda x: x['score'])

        print('Top 3 by Score:')
        for item in overall_rankings[:3]:
            pprint(f'Name: {item["name"]}')
            pprint(f'Score: {item["score"]}')
            pprint(f'Rating: {item["rating"]}')
            pprint(f'Price: {item["price"]}')
            # pprint(f'Reviews: {item["polar"]}')
