# Generated by Django 3.2.8 on 2021-11-04 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_alter_favorite_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='measurment_unit',
            new_name='measurement_unit',
        ),
    ]
