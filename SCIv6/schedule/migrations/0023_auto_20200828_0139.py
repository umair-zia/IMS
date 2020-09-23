# Generated by Django 3.1 on 2020-08-27 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0022_auto_20200828_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='exam',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='schedule.exam'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='room',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='schedule.room'),
        ),
    ]
