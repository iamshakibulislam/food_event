# Generated by Django 2.2.19 on 2021-03-27 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20210327_1728'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='events',
            unique_together={('start', 'mealPosition')},
        ),
    ]
