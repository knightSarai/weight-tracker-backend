# Generated by Django 3.2.9 on 2021-12-31 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lastname',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
