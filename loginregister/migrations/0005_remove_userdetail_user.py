# Generated by Django 4.2.6 on 2023-10-24 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginregister', '0004_userdetail_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetail',
            name='user',
        ),
    ]