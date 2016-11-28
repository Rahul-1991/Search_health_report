from config import Config
from service import PlayService


class SearchReport(object):

    def __init__(self):
        self.read_file_handle = open(Config.keyword_file, 'r')
        self.write_file_handle = open(Config.output_file, 'w')
        self.search_products = dict()
        self.play_service = PlayService()

    def _get_keyword_list(self):
        return [keyword.strip() for keyword in self.read_file_handle]

    @staticmethod
    def get_info_from_search(product_lite):
        required_fields = Config.search_fields
        return [product_lite.get(field, None) for field in required_fields]

    def get_info_from_pdp(self, product_lite):
        required_fields = Config.pdp_fields
        product_id = product_lite.get('entity_id')
        product_info = self.play_service.get_product_detail(product_id)
        return [product_info.get(field, None) for field in required_fields]

    def get_required_fields(self, keyword):
        product_info_list = list()
        self.search_products = self.play_service.get_products_for_keyword(keyword)
        product_list = self.search_products.get('data', [])
        for product in product_list:
            product.update({'totalProducts': self.search_products.get('totalProducts', 0),
                            'keyword': keyword})
            search_fields = self.get_info_from_search(product)
            print search_fields
            pdp_fields = self.get_info_from_pdp(product)
            product_info_list.append(search_fields + pdp_fields)
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
