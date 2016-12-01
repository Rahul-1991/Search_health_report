from coordinator import Coordinator
from config import Config


class PlayService(object):

    def __init__(self):
        self.coordinator = Coordinator()
        self.formatted_data = self.read_search_analytics_table()
        self.product_dict = self.get_info_by_product()

    def get_products_for_keyword(self, keyword):
        url = '/v2/getSearch'
        query_params = {'search': keyword, 'perPage': Config.perPage, 'abc': 123}
        response = self.coordinator.post(url, payload=query_params)
        return response.json().get('data', {}) if response.status_code == 200 else dict()

    def get_product_detail(self, product_id):
        url = '/product'
        params = {'productId': product_id}
        response = self.coordinator.get(url, payload=params)
        return response.json() if response.status_code == 200 else dict()

    def read_search_analytics_table(self):
        file_handle = open(Config.search_analytics_table, 'r')
        analytics_data = file_handle.readlines()
        formatted_data = [line.strip().split('\t') for line in analytics_data]
        return formatted_data

    def get_info_by_product(self):
        product_info = dict()
        for data in self.formatted_data:
            if data[1] in product_info:
                info = product_info.get(data[1])
                info.append(data)
                product_info[data[1]] = info
            else:
                product_info[data[1]] = [data]
        return product_info
