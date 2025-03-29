from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskUpdateView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)  # Register the TaskViewSet

urlpatterns = [
    # The router will automatically generate URL patterns for the task list and individual task detail
    path('', include(router.urls)),
    # Custom URL for task update
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
]
