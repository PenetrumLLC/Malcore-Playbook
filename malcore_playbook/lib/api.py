import malcore_playbook.lib.settings as settings

import requests


class Api(object):

    def __init__(self, only_remote=False):
        self.api_url = "https://api.malcore.io/api"
        self.auth_url = "https://api.malcore.io/auth"
        self.plan_url = "https://api.malcore.io/plan"
        if not only_remote:
            self.conf = settings.load_conf()
        else:
            self.conf = {}

    def upload_file(self, filename, endpoint):
        url = f"{self.api_url}/{endpoint}"
        files = {'filename1': open(filename, 'rb')}
        headers = {'apiKey': self.conf['api_key']}
        req = requests.post(url, files=files, headers=headers)
        try:
            return req.json()
        except:
            return None

    def login(self, username, password):
        post_data = {"email": username, "password": password}
        url = f"{self.auth_url}/login"
        try:
            req = requests.post(url, data=post_data)
            results = req.json()
        except:
            results = None
        import json
        with open('test.json', 'w') as fh:
            json.dump(results, fh, indent=4)
        return results

    def list_recipes(self):
        url = "https://recipes.malcore.io/assets/dbs/files.json"
        req = requests.get(url)
        data = req.json()
        return data
