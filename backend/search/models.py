from site import PREFIXES
from django.db import models
from django.contrib.auth.models import User
from feed.models import FeedPost
from core.models import PrefixedIDModel

class SearchQuery(PrefixedIDModel):
    id_prefix = "rsq-"
    DISCRETE = "discrete"
    PROMPT = "prompt"
    KIND_CHOICES = [
        (DISCRETE, "discrete"),
        (PROMPT, "prompt")
    ]

    USERS = "users"
    POSTS = "posts"
    ALL = "all"
    TARGET_CHOICES = [
        (USERS, "users"),
        (POSTS, "posts"),
        (ALL, "all")
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="searches")
    query_text = models.TextField()
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default=DISCRETE)
    target = models.CharField(max_length=10, choices=TARGET_CHOICES, default=ALL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query_text[:40]} ({self.kind})"

class SearchResult(PrefixedIDModel):
    id_prefix = "rsr-"
    search = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, related_name="results")
    rank = models.PositiveIntegerField()
    score = models.FloatField(null=True, blank=True)
    result_post = models.ForeignKey(FeedPost, on_delete=models.SET_NULL, null=True, blank=True, related_name="search_hits")
    result_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="search_hits")

    class Meta: #default sort order 
        ordering = ['rank']

    def __str__(self):
        return f"#{self.rank} for search {self.search_id}"