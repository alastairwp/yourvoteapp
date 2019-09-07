# Generated by Django 2.2.4 on 2019-09-04 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0017_usercourse'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name_plural': 'Sub-categories'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='question_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='question_number',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='subcategory_name',
            new_name='name',
        ),
    ]
