# Generated by Django 2.0 on 2019-09-24 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20190924_1949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='huifu',
            old_name='user_huifu_content',
            new_name='hf_content',
        ),
    ]