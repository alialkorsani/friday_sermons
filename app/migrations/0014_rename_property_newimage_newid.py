# Generated by Django 4.0.3 on 2022-03-30 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_token_id_alter_token_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newimage',
            old_name='property',
            new_name='NewId',
        ),
    ]
