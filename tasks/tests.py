from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Task
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token  # For token-based authentication


class TaskAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # If using token authentication, generate a token for the user
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # Set token in client

        self.url = reverse('task-list')  # Assuming 'task-list' is the name of your task list endpoint

    def test_create_task(self):
        """Test creating a new task via the API"""
        data = {'title': 'New Task', 'description': 'New Description', 'status': False, 'user': self.user.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_get_task(self):
        """Test retrieving tasks from the API"""
        task = Task.objects.create(title="Test Task", description="Description", status=False, user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_task(self):
        """Test updating a task via the API"""
        task = Task.objects.create(title="Test Task", description="Description", status=False, user=self.user)
        url = reverse('task-detail', args=[task.id])  # Assuming 'task-detail' is the URL name
        data = {'status': True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertTrue(task.status)

    def test_delete_task(self):
        """Test deleting a task via the API"""
        task = Task.objects.create(title="Test Task", description="Description", status=False, user=self.user)
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task.id)
