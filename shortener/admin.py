from django.contrib import admin

from shortener.models import URL

@admin.register(URL)
class ShortenedURLAdmin(admin.ModelAdmin):

    # Display the new fields in the admin list view
    list_display = ('original_url', 'short_code', 'created_at', 'clicks', 'last_accessed')
    search_fields = ('original_url', 'short_code')
    list_filter = ('created_at', 'last_accessed')
    readonly_fields = ('clicks', 'last_accessed')
