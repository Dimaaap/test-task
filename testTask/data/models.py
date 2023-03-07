from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()


class FakeCVSSchema(models.Model):
    author = models.ForeignKey(user_model, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, default='Untitled Schema')
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)