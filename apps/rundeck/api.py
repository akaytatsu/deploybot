import requests
from django.conf import settings
import json

class RundeckClient():

    def __init__(self):
        self.base_url = settings.RUNDECK_URL
        self.login()

    def request(self, method, url, querystring=None, payload=None, headers=None):
        response = requests.request(method, settings.RUNDECK_URL + url, data=payload, headers=headers, params=querystring)

        return response

    def login(self):
        data = {"j_username": settings.RUNDECK_USER_NAME, "j_password": settings.RUNDECK_USER_PASS}
        client = requests.Session()
        client.post(self.base_url + "/j_security_check", data=data)

        self.rundeckcli = client

    def list_jobs(self):
        response = self.rundeckcli.get(self.base_url + "/api/19/project/DEPLOY/jobs", headers={
            'Accept': "application/json"
        })

        return json.loads(response.text)

    def run_job(self, job_id):

        url = "/api/19/job/{}/run".format(job_id)

        response = self.rundeckcli.post(self.base_url + url, headers={
            'Accept': "application/json"
        })

        return json.loads(response.text)