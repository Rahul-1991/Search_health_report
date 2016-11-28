from coordinator import Coordinator
from config import Config


class PlayService(object):

    def __init__(self):
        self.coordinator = Coordinator()

    def get_products_for_keyword(self, keyword):
        url = '/v2/getSearch'
        query_params = {'search': keyword, 'perPage': Config.perPage}
        response = self.coordinator.post(url, payload=query_params)
        return response.json().get('data', {}) if response.status_code == 200 else dict()

    def get_product_detail(self, product_id):
        url = '/product'
        params = {'productId': product_id}
        response = self.coordinator.get(url, payload=params)
        return response.json() if response.status_code == 200 else dict()