# Generated by Django 4.1.3 on 2022-12-05 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_alter_tag_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=20),
        ),
    ]
