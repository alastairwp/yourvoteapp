# Generated by Django 2.2.4 on 2019-08-28 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0010_auto_20190828_1946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hint',
            old_name='hint_question_id',
            new_name='hint_question',
        ),
    ]
