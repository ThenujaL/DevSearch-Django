# Generated by Django 4.0.1 on 2022-02-13 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skills',
            name='description',
        ),
        migrations.AddField(
            model_name='skills',
            name='descriptioen',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
