# Generated by Django 3.2.4 on 2021-06-26 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource_share', '0003_auto_20210626_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentgrade',
            name='is_submit',
            field=models.BooleanField(null=True),
        ),
    ]
