# Generated by Django 4.0.3 on 2022-03-30 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_rename_property_newimage_newid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newimage',
            old_name='NewId',
            new_name='ItemId',
        ),
    ]
