# Generated by Django 4.1.3 on 2022-11-18 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_rename_username_profile_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='name',
            new_name='username',
        ),
    ]
