# Generated by Django 4.0.3 on 2022-03-30 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_token_id_alter_token_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='id',
        ),
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
