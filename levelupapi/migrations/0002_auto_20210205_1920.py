# Generated by Django 3.1.6 on 2021-02-05 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='scheduler_id',
            new_name='scheduler',
        ),
    ]
