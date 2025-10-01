# middleware.py

from django.utils.deprecation import MiddlewareMixin
from .models import RequestedUrls

class BlockedUrlsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Calculate the total number of blocked URLs
        self.total_blocked_urls = RequestedUrls.objects.filter(rejected=True).count()
        # Store the total blocked URLs in the request object
        print(self.total_blocked_urls)
        request.total_blocked_urls = self.total_blocked_urls
