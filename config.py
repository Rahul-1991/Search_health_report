import datetime


class Config(object):

    keyword_file = 'search_keywords'
    search_url = 'http://52.74.175.195:9193/v2/getSearch'
    required_fields = ['totalProducts', 'entity_id', 'relevance_score', '_score',
                       'price', 'discounted_price', 'vendor_name', 'image']
    output_file = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
