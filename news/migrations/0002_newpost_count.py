# Generated by Django 3.2.6 on 2022-02-08 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newpost',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
