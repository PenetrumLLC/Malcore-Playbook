#  Copyright (c) 2025.
#  Penetrum LLC (all rights reserved)
#  Copyright last updated: 5/2/25, 10:30 AM
#
#

import malcore_playbook.lib.settings as settings

import requests


class Api(object):

    """ malcore API object """

    def __init__(self, only_remote=False):
        self.api_url = "https://api.malcore.io/api"
        self.auth_url = "https://api.malcore.io/auth"
        self.plan_url = "https://api.malcore.io/plan"
        if not only_remote:
            self.conf = settings.load_conf()
        else:
            self.conf = {}

    def upload_file(self, filename, endpoint):
        """ uploada file to an endpoint """
        url = f"{self.api_url}/{endpoint}"
        files = {'filename1': open(filename, 'rb')}
        headers = {'apiKey': self.conf['api_key']}
        req = requests.post(url, files=files, headers=headers)
        try:
            return req.json()
        except:
            return None

    def login(self, username, password):
        """ login to the API to get the user API key and auth tokens """
        post_data = {"email": username, "password": password}
        url = f"{self.auth_url}/login"
        try:
            req = requests.post(url, data=post_data)
            results = req.json()
        except:
            results = None
        return results

    def list_recipes(self):
        """ gather a list of all available recipes """
        url = "https://recipes.malcore.io/assets/dbs/files.json"
        req = requests.get(url)
        data = req.json()
        return data

    def status_check(self, uuid):
        """ check the status of executable file analysis """
        url = f"{self.api_url}/status"
        data = {"uuid": uuid}
        headers = {'apiKey': self.conf['api_key']}
        req = requests.post(url, data=data, headers=headers)
        return req.json()
