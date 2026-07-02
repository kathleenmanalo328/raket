from django.contrib import admin
from .models import FeedPost, Comment, Like, CommentLike, PostBoost

admin.site.register(FeedPost)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(CommentLike)
admin.site.register(PostBoost)