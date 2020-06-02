# Generated by Django 2.1.8 on 2020-06-01 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmapData', '0003_auto_20200601_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.RemoveField(
            model_name='essay',
            name='like',
        ),
        migrations.RemoveField(
            model_name='essay',
            name='state',
        ),
        migrations.RemoveField(
            model_name='roadmap',
            name='like',
        ),
        migrations.AddField(
            model_name='essay',
            name='read_state',
            field=models.CharField(blank=True, default='unread', max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='read_state',
            field=models.CharField(blank=True, default='unread', max_length=200),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]