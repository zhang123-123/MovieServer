# Generated by Django 2.0 on 2019-09-17 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_movie'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='down',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='look',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='mark',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
