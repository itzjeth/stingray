# Generated by Django 3.2.24 on 2024-04-10 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_remove_userinfo_userimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cust',
            fields=[
                ('CustId', models.AutoField(primary_key=True, serialize=False)),
                ('CustFName', models.CharField(max_length=30)),
                ('CustEmail', models.CharField(max_length=50)),
                ('CustPass', models.CharField(max_length=60)),
            ],
            options={
                'db_table': 'FP_Cust',
            },
        ),
    ]
