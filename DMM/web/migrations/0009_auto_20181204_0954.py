# Generated by Django 2.1.3 on 2018-12-04 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20181204_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventurerrace',
            name='raceDescription',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adventurerrace',
            name='raceProficiencies',
            field=models.TextField(),
        ),
    ]