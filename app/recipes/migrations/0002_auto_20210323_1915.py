# Generated by Django 2.2.17 on 2021-03-23 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeoverview',
            name='url',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
