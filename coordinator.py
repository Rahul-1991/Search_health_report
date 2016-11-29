import requests
from config import Config


class Coordinator(object):

    def action(self, path):
        base_url = Config.base_url
        return base_url + path

    def post(self, path, payload={}, headers={}):
        response = requests.post(
            self.action(path), json=payload, headers=headers)
        return response

    def get(self, path, payload={}, headers={}):
        response = requests.get(
            self.action(path), params=payload, headers=headers)
        return response
