from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()


class FakeCVSSchema(models.Model):
    author = models.ForeignKey(user_model, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, default='Untitled Schema')
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class CVSSchemaFields(models.Model):
    DATA_TYPES_CHOICES = [
        (0, "Повне ім'я"),
        (1, "Робота"),
        (2, "Email"),
        (3, "Ім'я домену"),
        (4, "Номер телефону"),
        (5, "Назва компанії"),
        (6, "Текст"),
        (7, "Число"),
        (8, "Адреса"),
        (9, "Дата"),
    ]
    schema = models.ForeignKey(FakeCVSSchema, on_delete=models.CASCADE)
    field = models.IntegerField(choices=DATA_TYPES_CHOICES)
    name = models.CharField(max_length=255)
    order = models.IntegerField(blank=True, default=0)
    range_min = models.IntegerField(null=True, blank=True)
    range_max = models.IntegerField(null=True, blank=True)