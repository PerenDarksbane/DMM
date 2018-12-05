# Generated by Django 2.1.3 on 2018-12-05 01:09

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_auto_20181204_1953'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adventurer',
            old_name='stats',
            new_name='advStats',
        ),
        migrations.AddField(
            model_name='adventurer',
            name='advSpells',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
            preserve_default=False,
        ),
    ]