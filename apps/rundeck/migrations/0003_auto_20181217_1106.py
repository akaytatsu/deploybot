# Generated by Django 2.1.1 on 2018-12-17 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rundeck', '0002_jobs_use_chatbot'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobStatus',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('permalink', models.CharField(max_length=220)),
                ('status', models.CharField(max_length=30)),
                ('project', models.CharField(max_length=220)),
                ('message_id', models.CharField(max_length=30)),
                ('message_origin_user_id', models.CharField(max_length=120)),
                ('message_notified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterModelOptions(
            name='jobs',
            options={'verbose_name': 'Jobs', 'verbose_name_plural': 'Jobs'},
        ),
        migrations.AddField(
            model_name='jobstatus',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rundeck.Jobs'),
        ),
    ]
