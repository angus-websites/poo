from django.db import models

class Message(models.Model):
    slug = models.CharField(unique=True, max_length=10)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug
