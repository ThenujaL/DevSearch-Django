# Generated by Django 4.1.3 on 2022-12-18 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_review_owner_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
    ]
