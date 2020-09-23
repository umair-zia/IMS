# Generated by Django 3.1 on 2020-09-03 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0024_auto_20200828_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='certificateSchedule',
            field=models.IntegerField(default=None),
        ),
        migrations.RemoveField(
            model_name='exam',
            name='registrationSchedule',
        ),
        migrations.AddField(
            model_name='exam',
            name='registrationSchedule',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='exam',
            name='resultSchedule',
            field=models.IntegerField(default=None),
        ),
    ]
