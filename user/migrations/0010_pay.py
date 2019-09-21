# Generated by Django 2.0 on 2019-09-20 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20190919_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('out_trade_no', models.CharField(max_length=50)),
                ('trade_no', models.CharField(max_length=50)),
                ('user_id', models.IntegerField()),
                ('pay_date', models.DateTimeField(auto_now_add=True)),
                ('pay_price', models.FloatField()),
                ('pay_status', models.IntegerField()),
            ],
        ),
    ]
