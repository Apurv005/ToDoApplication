from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Task

# Register your Task model with the admin site
admin.site.register(Task)
