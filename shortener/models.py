from django.db import models
from django.utils import timezone


class URL(models.Model):
    """
    The main model for storing URL shortening data.
    """

    original_url = models.URLField()                            # Original URL
    short_code = models.CharField(max_length=10, unique=True)   # Short code for the URL
    created_at = models.DateTimeField(auto_now_add=True)        # Creation timestamp
    hide_preview = models.BooleanField(default=False)           # Require click before redirecting

    last_accessed = models.DateTimeField(null=True, blank=True) # Last accessed timestamp
    clicks = models.PositiveIntegerField(default=0)             # Number of times the URL was accessed

    def __str__(self):
        return f'{self.short_code} -> {self.original_url}'

    def record_access(self):
        """
        Every time the URL is accessed
        this method should be called to update
        the last accessed timestamp and the number of clicks.
        """
        self.last_accessed = timezone.now()
        self.clicks += 1
        self.save(update_fields=['last_accessed', 'clicks'])

