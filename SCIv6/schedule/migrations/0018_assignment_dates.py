# Generated by Django 3.1 on 2020-08-27 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0017_auto_20200825_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='dates',
            field=models.TextField(default=None),
        ),
    ]
