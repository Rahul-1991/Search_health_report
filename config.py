import datetime


class Config(object):

    keyword_file = 'search_keywords'
    base_url = 'http://52.74.175.195:9195'
    search_fields = ['keyword', 'totalProducts', 'entity_id', 'relevance_score', '_score', 'price', 'discounted_price',
                     'vendor_name', 'image']
    pdp_fields = ['seller_ratings', 'attributes', 'gallery_images', 'category_name']
    output_file = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    perPage = 100
    search_analytics_table = 'last_20_days_data.csv'
