# Generated by Django 2.2.4 on 2019-09-02 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0014_auto_20190828_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
