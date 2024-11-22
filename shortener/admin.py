from django.contrib import admin

from shortener.models import URL


# Register your models here.
# Register the model with the admin site
@admin.register(URL)
class ShortenedURLAdmin(admin.ModelAdmin):
    # Optional: Customize the admin list display
    list_display = ('original_url', 'short_code', 'created_at')
    search_fields = ('original_url', 'short_code')
    list_filter = ('created_at',)
