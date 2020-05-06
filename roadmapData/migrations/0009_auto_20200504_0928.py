# Generated by Django 2.1.8 on 2020-05-04 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadmapData', '0008_auto_20200504_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200)),
                ('articles', models.ManyToManyField(blank=True, to='roadmapData.Article')),
                ('essays', models.ManyToManyField(blank=True, to='roadmapData.Essay')),
                ('roadmaps', models.ManyToManyField(blank=True, to='roadmapData.RoadMap')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='articletag',
            name='articles',
        ),
        migrations.RemoveField(
            model_name='articletag',
            name='user',
        ),
        migrations.RemoveField(
            model_name='essaytag',
            name='essays',
        ),
        migrations.RemoveField(
            model_name='essaytag',
            name='user',
        ),
        migrations.RemoveField(
            model_name='roadmaptag',
            name='roadmaps',
        ),
        migrations.RemoveField(
            model_name='roadmaptag',
            name='user',
        ),
        migrations.DeleteModel(
            name='ArticleTag',
        ),
        migrations.DeleteModel(
            name='EssayTag',
        ),
        migrations.DeleteModel(
            name='RoadMapTag',
        ),
    ]
