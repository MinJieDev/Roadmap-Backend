# Generated by Django 3.0.5 on 2020-04-17 02:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roadmapData', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='user',
        ),
        migrations.AlterField(
            model_name='article',
            name='article_references',
            field=models.ManyToManyField(blank=True, null=True, related_name='_article_article_references_+', to='roadmapData.Article'),
        ),
        migrations.AlterField(
            model_name='essay',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='roadmap',
            name='articles',
            field=models.ManyToManyField(blank=True, null=True, to='roadmapData.Article'),
        ),
        migrations.AlterField(
            model_name='roadmap',
            name='essays',
            field=models.ManyToManyField(blank=True, null=True, to='roadmapData.Essay'),
        ),
        migrations.AlterField(
            model_name='roadmap',
            name='road_maps',
            field=models.ManyToManyField(blank=True, null=True, related_name='_roadmap_road_maps_+', to='roadmapData.RoadMap'),
        ),
        migrations.AlterField(
            model_name='roadmap',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ReadRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_state', models.BooleanField(blank=True, default=False)),
                ('text', models.TextField(blank=True, default='')),
                ('article', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='roadmapData.Article')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
