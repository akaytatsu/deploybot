from django.db import models

# Create your models here.
class Jobs(models.Model):
    id = models.CharField(max_length=100, blank=False, null=False, unique=True, primary_key=True)
    href = models.CharField(max_length=220, blank=False, null=False)
    enabled = models.BooleanField(blank=False, null=False, default=False)
    permalink = models.CharField(max_length=220, blank=False, null=False)
    name = models.CharField(max_length=220, blank=False, null=False)
    project = models.CharField(max_length=220, blank=False, null=False)
    description = models.TextField()
    use_chatbot = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        verbose_name = "Jobs"
        verbose_name_plural = "Jobs"

class JobStatus(models.Model):
    id = models.IntegerField(blank=False, null=False, unique=True, primary_key=True)
    permalink = models.CharField(max_length=220, blank=False, null=False)
    status = models.CharField(max_length=30, blank=False, null=False)
    project = models.CharField(max_length=220, blank=False, null=False)
    job = models.ForeignKey(Jobs, null=False, blank=False, on_delete=models.CASCADE)
    message_id = models.CharField(max_length=30, null=False, blank=False)
    message_origin_user_id = models.CharField(max_length=120, null=False, blank=False)
    message_notified = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name = "Job Status"
        verbose_name_plural = "Job Status"