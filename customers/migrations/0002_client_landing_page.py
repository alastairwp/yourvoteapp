# Generated by Django 2.2.6 on 2019-11-17 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='landing_page',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
