from config import Config
import requests


class SearchReport(object):

    def __init__(self):
        self.read_file_handle = open(Config.keyword_file, 'r')
        self.write_file_handle = open(Config.output_file, 'w')

    def _get_keyword_list(self):
        return [keyword.strip() for keyword in self.read_file_handle]

    @staticmethod
    def get_products_for_keyword(keyword):
        url = Config.search_url
        query_params = {'search': keyword, 'perPage': Config.perPage}
        response = requests.post(url, json=query_params)
        return response.json().get('data', {})

    def get_required_fields(self, keyword):
        required_fields = Config.required_fields
        product_info_list = list()
        search_response = self.get_products_for_keyword(keyword)
        product_list = search_response.get('data', [])
        for product in product_list:
            product.update({'totalProducts': search_response.get('totalProducts', 0)})
            product_info = [keyword]
            for field in required_fields:
                product_info.append(str(product.get(field, None)))
            product_info_list.append(product_info)
        return product_info_list

    def print_to_file(self, keyword_info):
        for info in keyword_info:
            self.write_file_handle.write(','.join(info)+'\n')

    def main(self):
        keywords_list = self._get_keyword_list()
        for keyword in keywords_list:
            fields = self.get_required_fields(keyword)
            self.print_to_file(fields)
        self.read_file_handle.close()
        self.write_file_handle.close()


report = SearchReport()
report.main()
