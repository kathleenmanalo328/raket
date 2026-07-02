from django.contrib import admin
from .models import SearchQuery, SearchResult

admin.site.register(SearchQuery)
admin.site.register(SearchResult)