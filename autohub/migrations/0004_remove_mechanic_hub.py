# Generated by Django 4.2.6 on 2023-11-22 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autohub', '0003_mechanic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mechanic',
            name='hub',
        ),
    ]
