# Generated by Django 4.1.3 on 2024-03-06 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roleapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='image',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
