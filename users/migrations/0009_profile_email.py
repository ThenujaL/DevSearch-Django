# Generated by Django 4.0.1 on 2022-02-14 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_rename_descriptioen_skills_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=80, null=True),
        ),
    ]
