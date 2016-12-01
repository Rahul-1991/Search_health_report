from config import Config
from service import PlayService
from datetime import datetime
import math

ORDER_COLUMN = 2
VISITS_COLUMN = 4

class SearchReport(object):

    def __init__(self):
        self.read_file_handle = open(Config.keyword_file, 'r')
        self.write_file_handle = open(Config.output_file, 'w')
        self.search_products = dict()
        self.play_service = PlayService()

    def get_recency_score(self, product_info):
        if not product_info[0]:
            return False
        sorted_product_info = sorted(product_info, key=lambda x: x[0], reverse=True)
        last_accessed_date_object = datetime.strptime(sorted_product_info[0][0], '%Y-%m-%d')
        current_time_object = datetime.now()
        last_update_difference = (current_time_object - last_accessed_date_object).days
        if last_update_difference > 3:
            return False
        exp_distance = max(0, last_update_difference-1)
        exp_lambda = math.log10(0.5) / 10
        return math.exp(exp_distance * exp_lambda)

    def get_performance_score(self, sold, clicks):
        if not int(clicks):
            return 0
        product_conversion_score = int(sold)/int(clicks)
        return product_conversion_score + (int(sold) / 5)

    def get_relevance_score(self, product_info, total_orders, total_visits, seller_rating):
        recency_score = self.get_recency_score(product_info)
        performance_score = self.get_performance_score(total_orders, total_visits)
        return str(0.05 * recency_score  + 0.75 * performance_score + 0.5 * float(seller_rating))

    def _get_keyword_list(self):
        return [keyword.strip() for keyword in self.read_file_handle]

    def _get_info_for_product(self, product_info, column):
        if not product_info[0]:
            return '0'
        sum = 0
        for info in product_info:
            sum += int(info[column])
        return str(sum)

    def get_info_from_redshift(self, product):
        product_id = product.get('entity_id')
        product_info = self.play_service.product_dict.get(str(product_id), [[]])
        total_orders = self._get_info_for_product(product_info, ORDER_COLUMN)
        total_visits = self._get_info_for_product(product_info, VISITS_COLUMN)
        seller_rating = product.get('seller_ratings', 0)
        calculated_relevance_score = self.get_relevance_score(product_info, total_orders, total_visits, seller_rating)
        return [total_orders, total_visits, calculated_relevance_score]


    @staticmethod
    def get_info_from_search(product_lite):
        required_fields = Config.search_fields
        return [str(product_lite.get(field, None)) for field in required_fields]

    def get_info_from_pdp(self, product_lite):
        required_fields = Config.pdp_fields
        product_id = product_lite.get('entity_id')
        product_info = self.play_service.get_product_detail(product_id)
        field_info = list()
        for field in required_fields:
            if field == 'attributes':
                field_info.append(str(product_info.get(field, [])))
                field_info.append(str(len(product_info.get(field, []))))
            elif field == 'gallery_images':
                field_info.append(str(len(product_info.get(field, '').strip(',').split(','))))
            elif field == 'category_name':
                field_info.append(str(product_info.get(field, [])[-2:]))
            else:
                field_info.append(str(product_info.get(field, None)))
        return field_info

    def get_required_fields(self, keyword):
        product_info_list = list()
        self.search_products = self.play_service.get_products_for_keyword(keyword)
        product_list = self.search_products.get('data', [])
        for product in product_list:
            product.update({'totalProducts': self.search_products.get('totalProducts', 0),
                            'keyword': keyword})
            search_fields = self.get_info_from_search(product)
            pdp_fields = self.get_info_from_pdp(product)
            redshift_fields = self.get_info_from_redshift(product)
            product_info_list.append(search_fields + pdp_fields + redshift_fields)
        return product_info_list

    def print_to_file(self, keyword_info):
        for info in keyword_info:
            self.write_file_handle.write('$$$'.join(info)+'\n')

    def main(self):
        keywords_list = self._get_keyword_list()
        for keyword in keywords_list:
            print keyword
            fields = self.get_required_fields(keyword)
            self.print_to_file(fields)
        self.read_file_handle.close()
        self.write_file_handle.close()


report = SearchReport()
report.main()
