# Generated by Django 2.2.4 on 2019-09-30 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0023_auto_20190923_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_subcat', to='benchmark.SubCategory'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcat_cat', to='benchmark.Category'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='question',
            field=models.ForeignKey(on_delete=models.SET(0), related_name='vote_question', to='benchmark.Question'),
        ),
    ]