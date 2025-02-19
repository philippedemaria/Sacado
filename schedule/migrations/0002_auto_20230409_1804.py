# Generated by Django 3.0.5 on 2023-04-09 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0008_auto_20230202_1527'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_allday',
        ),
        migrations.RemoveField(
            model_name='event',
            name='notification',
        ),
        migrations.RemoveField(
            model_name='event',
            name='notification_day',
        ),
        migrations.RemoveField(
            model_name='event',
            name='type_of_event',
        ),
        migrations.CreateModel(
            name='Slotedt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='start')),
                ('stop', models.DateTimeField(verbose_name='stop')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Contenu')),
                ('groups', models.ManyToManyField(blank=True, editable=False, related_name='slots_edt', to='group.Group')),
                ('user', models.ManyToManyField(blank=True, related_name='my_slots_edt', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Edt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_slot', models.BooleanField(default=0)),
                ('is_saturday', models.BooleanField(default=1)),
                ('is_wednesday', models.BooleanField(default=0)),
                ('start', models.DateTimeField(verbose_name='start')),
                ('stop', models.DateTimeField(verbose_name='stop')),
                ('slots', models.ManyToManyField(blank=True, editable=False, related_name='edts', to='schedule.Slotedt')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_edts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
