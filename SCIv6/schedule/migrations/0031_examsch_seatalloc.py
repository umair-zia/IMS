# Generated by Django 3.1 on 2020-09-16 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0030_auto_20200915_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='EXAMSCH',
            fields=[
                ('RECID', models.AutoField(primary_key=True, serialize=False)),
                ('EXAMCODE', models.CharField(max_length=10)),
                ('EXAMMEDIUM', models.CharField(max_length=1)),
                ('EXAMMODE', models.CharField(max_length=1)),
                ('EXAMDATE', models.IntegerField()),
                ('REGDATE', models.IntegerField()),
                ('RESULTDATE', models.IntegerField()),
                ('CERTDATE', models.IntegerField()),
                ('SESSIONID', models.CharField(max_length=5)),
                ('VENUEID', models.CharField(max_length=5)),
                ('ROOMID', models.CharField(max_length=5)),
                ('CAPACITY', models.IntegerField()),
                ('FILLED', models.IntegerField()),
                ('SUBCODE', models.CharField(max_length=10)),
                ('SEATNO', models.IntegerField()),
                ('INVIGILATOR', models.CharField(max_length=12)),
                ('CREATED', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SEATALLOC',
            fields=[
                ('RECID', models.AutoField(primary_key=True, serialize=False)),
                ('EXAMCODE', models.CharField(max_length=10)),
                ('SUBCODE', models.CharField(max_length=10)),
                ('EXAMMEDIUM', models.CharField(max_length=1)),
                ('EXAMMODE', models.CharField(max_length=1)),
                ('SESSIONID', models.CharField(max_length=5)),
                ('COMPANYID', models.CharField(max_length=12)),
                ('VENUEID', models.CharField(max_length=5)),
                ('ROOMID', models.CharField(max_length=5)),
                ('RESERVERDFOR', models.CharField(max_length=1)),
                ('Assessor', models.CharField(max_length=50)),
                ('CourseCode', models.CharField(max_length=12)),
            ],
        ),
    ]
