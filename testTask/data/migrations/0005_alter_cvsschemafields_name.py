# Generated by Django 4.1.7 on 2023-03-07 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_cvsschemafields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvsschemafields',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
