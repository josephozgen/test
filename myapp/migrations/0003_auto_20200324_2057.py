# Generated by Django 2.2 on 2020-03-25 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_event'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Event',
            new_name='Item',
        ),
        migrations.AddField(
            model_name='user',
            name='date_hired',
            field=models.DateField(null=True),
        ),
    ]
