# Generated by Django 4.1.3 on 2022-11-26 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_profile_username'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Skills',
            new_name='Skill',
        ),
    ]
