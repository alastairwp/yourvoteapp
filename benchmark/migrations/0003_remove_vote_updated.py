# Generated by Django 2.2.2 on 2019-08-21 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0002_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='updated',
        ),
    ]
