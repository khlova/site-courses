# Generated by Django 3.1.5 on 2021-01-10 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20210110_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='free',
            field=models.BooleanField(default=True),
        ),
    ]
