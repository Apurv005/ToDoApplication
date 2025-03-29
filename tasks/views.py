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

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        """
        Custom action to update the status of the task (completed or not)
        """
        task = self.get_object()
        task.status = not task.status  # Toggle status
        task.save()
        return Response({'status': task.status})

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  # Show only logged-in user's tasks

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Save task with logged-in user