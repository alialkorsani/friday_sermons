# Generated by Django 4.0.3 on 2022-03-31 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_rename_lecture_lecturevideo_item_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fridaysermonvideo',
            old_name='property',
            new_name='item',
        ),
    ]
