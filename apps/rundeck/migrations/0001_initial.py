# Generated by Django 2.1.1 on 2018-12-15 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('href', models.CharField(max_length=220)),
                ('enabled', models.BooleanField(default=False)),
                ('permalink', models.CharField(max_length=220)),
                ('name', models.CharField(max_length=220)),
                ('project', models.CharField(max_length=220)),
                ('description', models.TextField()),
            ],
        ),
    ]
