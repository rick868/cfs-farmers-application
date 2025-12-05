from django.db import models

class PolicyDocument(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    region = models.CharField(max_length=100, help_text="e.g. National, Nakuru County")
    category = models.CharField(max_length=100)
    external_link = models.URLField(blank=True, null=True)
    file_upload = models.FileField(upload_to='policy_docs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
