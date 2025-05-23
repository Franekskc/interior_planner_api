# Generated by Django 5.1.7 on 2025-03-25 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('model_3d', models.FileField(upload_to='local_models/')),
                ('thumbnail', models.ImageField(upload_to='local_thumbnails/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('firebase_model_url', models.URLField(blank=True)),
                ('firebase_thumbnail_url', models.URLField(blank=True)),
            ],
        ),
    ]
