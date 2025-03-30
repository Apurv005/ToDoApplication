from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}

    completed = serializers.BooleanField(required=False)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  # Auto-assign user
        return super().create(validated_data)