# Generated by Django 4.0.3 on 2022-03-25 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_alter_token_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='auth', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
