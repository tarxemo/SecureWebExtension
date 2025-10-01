from django.db import models

class RestrictedURL(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url

class RestrictedKeyword(models.Model):
    keyword = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.keyword
    
class RequestedUrls(models.Model):
    url = models.ForeignKey(RestrictedURL, on_delete=models.CASCADE, null=True, blank=True)
    keyword = models.ForeignKey(RestrictedKeyword, on_delete=models.CASCADE, null=True, blank=True)
    unblocked_url = models.URLField(null=True, blank=True)
    visited_at = models.DateTimeField(auto_now_add = True)
    rejected = models.BooleanField(default=False)
