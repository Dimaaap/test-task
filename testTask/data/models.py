from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()


class FakeCVSSchema(models.Model):
    # POSSIBLE_DELIMITERS = (
    #     (',', 'Кома(,)'),
    #     (';', 'Крапка з комою(;)'),
    #     ('\t', 'Табуляція(\\t)'),
    #     (" ", "Пробіл(' ')"),
    #     ("|", "Вертикальна палочка('|')")
    # )
    author = models.ForeignKey(user_model, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, default='Untitled Schema')
    #delimiter = models.CharField(max_length=1, choices=POSSIBLE_DELIMITERS, default=',')
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class CVSSchemaFields(models.Model):
    DATA_TYPES_CHOICES = [
        ("Повне ім'я", "Повне ім'я"),
        ("Робота", "Робота"),
        ("Email", "Email"),
        ("Ім'я домену", "Ім'я домену"),
        ("Номер телефону", "Номер телефону"),
        ("Назва компанії", "Назва компанії"),
        ("Текст", "Текст"),
        ("Число", "Число"),
        ("Адреса", "Адреса"),
        ("Дата", "Дата"),
    ]
    schema = models.ForeignKey(FakeCVSSchema, on_delete=models.CASCADE)
    field = models.CharField(choices=DATA_TYPES_CHOICES, max_length=30, default='Дата')
    name = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(blank=True, default=0, null=True)
    range_min = models.PositiveIntegerField(null=True, blank=True)
    range_max = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name or 'Поле без назви'
