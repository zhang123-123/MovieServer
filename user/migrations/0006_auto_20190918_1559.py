# Generated by Django 2.0 on 2019-09-18 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_movie_vip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='vip',
        ),
        migrations.AddField(
            model_name='pythonuser',
            name='vip',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
