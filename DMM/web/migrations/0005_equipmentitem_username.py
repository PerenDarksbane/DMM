# Generated by Django 2.1.3 on 2018-12-03 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_remove_equipmentitem_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentitem',
            name='userName',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='web.UserProfile'),
            preserve_default=False,
        ),
    ]