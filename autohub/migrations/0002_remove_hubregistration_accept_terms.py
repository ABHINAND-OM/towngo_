# Generated by Django 4.2.6 on 2023-10-23 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autohub', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hubregistration',
            name='accept_terms',
        ),
    ]