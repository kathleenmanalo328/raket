from rest_framework import viewsets
from .models import FeedPost, Comment, Like
from .serializers import FeedPostSerializer, CommentSerializer, LikeSerializer

class FeedPostViewSet(viewsets.ModelViewSet):
    queryset = FeedPost.objects.all()
    serializer_class = FeedPostSerializer
    filterset_fields = ["media_type", "author"]
    search_fields = ["caption"]
    ordering_fields = ["created_at"]

    # For now posts are public and author stays empty.
    # Once auth is enabled (lesson 05), uncomment this to stamp the logged-in user:
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)