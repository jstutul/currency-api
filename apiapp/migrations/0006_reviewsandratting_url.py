# Generated by Django 5.0.2 on 2024-02-24 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0005_reviewsandratting'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewsandratting',
            name='url',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
