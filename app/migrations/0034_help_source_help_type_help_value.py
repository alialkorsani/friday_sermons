# Generated by Django 4.0.3 on 2022-04-13 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_delete_aidchart'),
    ]

    operations = [
        migrations.AddField(
            model_name='help',
            name='source',
            field=models.CharField(choices=[('A', 'Ataba'), ('M', 'Maktab')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='help',
            name='type',
            field=models.CharField(choices=[('MG', 'Merage'), ('B', 'Build'), ('D', 'Debit'), ('O', 'Other'), ('MD', 'Medical'), ('S', 'Sale'), ('R', 'Rent')], default='O', max_length=2),
        ),
        migrations.AddField(
            model_name='help',
            name='value',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
