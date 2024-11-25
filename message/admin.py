from django.contrib import admin
from django.template.defaultfilters import truncatechars

from message.models import Message


@admin.register(Message)
class MessageURLAdmin(admin.ModelAdmin):

    # Define a method to truncate content
    def short_content(self, obj):
        return truncatechars(obj.content, 35)

    short_content.short_description = 'Short Content'  # Optional: Customize the column header

    # Display the new fields in the admin list view
    list_display = ('slug', 'short_content', 'created_at')
    search_fields = ('slug', 'content')
    list_filter = ['created_at']

