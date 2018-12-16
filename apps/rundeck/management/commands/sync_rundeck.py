from django.core.management.base import BaseCommand
from apps.rundeck.api import RundeckClient
from apps.rundeck.models import Jobs

class Command(BaseCommand):
    help = 'Start bot for listen'

    def handle(self, *args, **kwargs):
        print("Started Rundeck Sync")

        rundeckcli = RundeckClient()
        list_jobs = rundeckcli.list_jobs()

        for job_json in list_jobs:
            try:
                job = Jobs.objects.get(id=job_json.get("id"))
            except Jobs.DoesNotExist:
                job = Jobs()

            job.id = job_json.get("id")
            job.name = job_json.get("name")
            job.description = job_json.get("description")
            job.enabled = job_json.get("enabled")
            job.href = job_json.get("href")
            job.permalink = job_json.get("permalink")
            job.project = job_json.get("project")
            job.save()

