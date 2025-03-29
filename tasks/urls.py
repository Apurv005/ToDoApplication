from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)  # Register the TaskViewSet

urlpatterns = router.urls  # The router will automatically handle the URL paths for the tasks API

