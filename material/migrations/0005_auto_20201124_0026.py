# Generated by Django 3.1.1 on 2020-11-23 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0004_auto_20201121_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='explanation_en',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='answer',
            name='explanation_fi',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]