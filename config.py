import datetime


class Config(object):

    keyword_file = 'search_keywords'
    base_url = 'http://52.74.175.195:9193'
    search_fields = ['keyword', 'totalProducts', 'entity_id', 'relevance_score', '_score', 'price', 'discounted_price',
                     'vendor_name', 'image']
    pdp_fields = ['attributes', 'gallery_images']
    output_file = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    perPage = 100
