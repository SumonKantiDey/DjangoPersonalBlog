# Generated by Django 2.2.2 on 2019-06-28 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='approaved_comment',
            new_name='approved_comment',
        ),
    ]
