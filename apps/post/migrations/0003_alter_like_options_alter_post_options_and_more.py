# Generated by Django 4.1.3 on 2023-01-07 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'ordering': ('id',), 'verbose_name': 'Лайкнутый', 'verbose_name_plural': 'Лайкнутые'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-create_at',), 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterModelOptions(
            name='postimage',
            options={'ordering': ('-id',), 'verbose_name': 'Картинка к посту', 'verbose_name_plural': 'Картинки к посту'},
        ),
        migrations.AlterModelOptions(
            name='save',
            options={'ordering': ('id',), 'verbose_name': 'Сохранённое', 'verbose_name_plural': 'Сохранённые'},
        ),
    ]