# Generated by Django 3.0.5 on 2023-01-08 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0006_group_is_gar'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_hidden',
            field=models.BooleanField(default=0),
        ),
    ]
