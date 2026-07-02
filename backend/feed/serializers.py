from rest_framework import serializers
from .models import FeedPost, Comment, Like

class FeedPostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = FeedPost
        fields = [
            "id", 
            "author", 
            "author_username", 
            "caption",
            "file",
            "media_type",
            "job_post",
            "likes_count",
            "shares_count",
            "reposts_count",
            "created_at",
        ]
        read_only_fields = [
            "id", 
            "author", 
            "media_type",
            "job_post",
            "shares_count",
            "reposts_count",
            "created_at",
            ]

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "author_username", "parent", "text", "created_at"]
        read_only_fields = ["id", "author", "created_at"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]