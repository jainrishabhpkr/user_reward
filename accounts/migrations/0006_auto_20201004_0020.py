# Generated by Django 2.2 on 2020-10-03 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201003_1343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='level',
            options={'ordering': ('min_point',)},
        ),
        migrations.RemoveField(
            model_name='level',
            name='level_heirarchy',
        ),
        migrations.AddField(
            model_name='level',
            name='max_point',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='level',
            name='min_point',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
