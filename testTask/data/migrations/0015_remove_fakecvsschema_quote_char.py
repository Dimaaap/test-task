# Generated by Django 4.1.7 on 2023-03-08 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_alter_fakecvsschema_delimiter_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fakecvsschema',
            name='quote_char',
        ),
    ]
