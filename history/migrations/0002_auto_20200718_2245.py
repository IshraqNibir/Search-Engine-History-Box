# Generated by Django 3.0.7 on 2020-07-18 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
