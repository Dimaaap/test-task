# Generated by Django 4.1.7 on 2023-03-07 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_alter_cvsschemafields_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvsschemafields',
            name='field',
            field=models.CharField(choices=[("Повне ім'я", "Повне ім'я"), ('Робота', 'Робота'), ('Email', 'Email'), ("Ім'я домену", "Ім'я домену"), ('Номер телефону', 'Номер телефону'), ('Назва компанії', 'Назва компанії'), ('Текст', 'Текст'), ('Число', 'Число'), ('Адреса', 'Адреса'), ('Дата', 'Дата')], max_length=30),
        ),
    ]
