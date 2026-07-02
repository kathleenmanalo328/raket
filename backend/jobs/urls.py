from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, SavedJobViewSet

router = DefaultRouter()
router.register("applications", JobApplicationViewSet, basename="application")
router.register("saved", SavedJobViewSet, basename="savedjob")

urlpatterns = router.urls
