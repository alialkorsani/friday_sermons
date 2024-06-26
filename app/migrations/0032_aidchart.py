# Generated by Django 4.0.3 on 2022-04-11 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_remove_bookpdf_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='AidChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_text', models.CharField(max_length=50)),
                ('total_number', models.IntegerField()),
                ('title_1', models.CharField(max_length=50)),
                ('desc_1', models.CharField(max_length=50)),
                ('end_value_1', models.IntegerField()),
                ('all_value_1', models.IntegerField()),
                ('title_2', models.CharField(max_length=50)),
                ('desc_2', models.CharField(max_length=50)),
                ('end_value_2', models.IntegerField()),
                ('all_value_2', models.IntegerField()),
                ('title_3', models.CharField(max_length=50)),
                ('desc_3', models.CharField(max_length=50)),
                ('end_value_3', models.IntegerField()),
                ('all_value_3', models.IntegerField()),
            ],
        ),
    ]
