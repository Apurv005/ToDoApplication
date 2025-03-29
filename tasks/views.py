from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        """
        Limit the tasks to only those belonging to the authenticated user
        """
        return Task.objects.filter(user=self.request.user)

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        """
        Custom action to update the status of the task (completed or not)
        """
        task = self.get_object()
        task.status = not task.status  # Toggle status
        task.save()
        return Response({'status': task.status})

    def perform_create(self, serializer):
        """
        Override the perform_create method to automatically associate the task with the logged-in user
        """
        serializer.save(user=self.request.user)

