from django.db import models
from django.utils import timezone

# Create your models here.

class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    last_accessed = models.DateTimeField(null=True, blank=True)
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.short_code} -> {self.original_url}'

    # Method to update access info
    def record_access(self):
        self.last_accessed = timezone.now()
        self.clicks += 1
        self.save(update_fields=['last_accessed', 'clicks'])

