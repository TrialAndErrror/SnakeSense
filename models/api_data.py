from yelpapi import YelpAPI
from .restaurant import Restaurant
from pprint import pprint
from pathlib import Path
from utils import make_data_path, load_json, save_json
from sys import exit
from json.decoder import JSONDecodeError
from json.encoder import JSONEncoder
from slugify import slugify


class CustomEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class YelpDataGatherer:
    data_path: Path
    yelp_obj: YelpAPI
    restaurants: list = []
    business_list: list = []

    def __init__(self):
        self.data_path = make_data_path()
        self.create_yelp_api_obj()

    def create_yelp_api_obj(self):
        try:
            api_key = load_json(Path(self.data_path.parent, 'api_config.json')).get('API_KEY')
        except FileNotFoundError:
            print('Error: Please provide API key in an api_config.json file in the root directory.')
            exit()
        except JSONDecodeError:
            print('Error: Please provide valid API key in an api_config.json file in the root directory.')
            exit()
        else:
            self.yelp_obj = YelpAPI(api_key, timeout_s=3.0)

    def search_for_restaurants(self):
        """
        Get all restaurants that mention that they serve fried chicken.
        """

        business_list_path = Path(self.data_path, 'business_list.json')
        if business_list_path.exists():
            print('Loading Restaurant Data...')
            self.business_list = load_json(business_list_path)
        else:
            print('Searching for Restaurants...')
            results = self.yelp_obj.search_query(
                term="\"fried chicken\"",
                location="arkansas",
                category="bbq,chicken_shop,chinese,chicken_wings,soulfood",
                limit=50
            )

            self.business_list = results['businesses']
            save_json(business_list_path, self.business_list)

    def process_all_restaurants(self):
        print('Processing Restaurants...')
        reviews_folder = Path(self.data_path, 'reviews')
        reviews_folder.mkdir(parents=True, exist_ok=True)
        for item in self.business_list:
            slug_name = slugify(item.get('name'))
            reviews_path = Path(reviews_folder, f"{slug_name}-reviews.json")
            new_restaurant = Restaurant(self.yelp_obj, reviews_path)
            new_restaurant.ingest_data(item)
            self.restaurants.append(new_restaurant)
            new_restaurant.get_reviews()
            new_restaurant.process_reviews()

    def get_rankings(self):
        print('Calculating Rankings')
        overall_rankings = []
        for item in self.restaurants:
            results = item.get_results()
            overall_rankings.append(results)
        overall_rankings.sort(key=lambda x: x['score'], reverse=True)

        print('Top 5 by Score:')
        for item in overall_rankings[:5]:
            pprint(f'Name: {item["name"]}')
            pprint(f'Score: {item["score"]}')
            pprint(f'Rating: {item["rating"]}')
            pprint(f'Price: {item["price"]}')

        save_json(Path(self.data_path, 'overall_results.json'), overall_rankings[:5], cls=CustomEncoder)
