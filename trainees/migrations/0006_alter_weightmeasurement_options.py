# Generated by Django 3.2.9 on 2021-12-31 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainees', '0005_alter_trainee_trainer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weightmeasurement',
            options={'ordering': ['-user_input_date']},
        ),
    ]