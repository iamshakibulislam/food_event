# Generated by Django 2.2.19 on 2021-03-27 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20210327_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='likedIt',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='events',
            name='notLiked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='events',
            name='notMade',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='events',
            unique_together=set(),
        ),
    ]
