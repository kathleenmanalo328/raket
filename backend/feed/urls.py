from rest_framework.routers import DefaultRouter
from .views import FeedPostViewSet, CommentViewSet, LikeViewSet

router = DefaultRouter()
router.register("posts", FeedPostViewSet, basename="feedpost")
router.register("comments", CommentViewSet, basename="comment")
router.register("likes", LikeViewSet, basename="like")

urlpatterns = router.urls
