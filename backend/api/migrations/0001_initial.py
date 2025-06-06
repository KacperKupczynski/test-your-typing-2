# Generated by Django 5.1.4 on 2025-06-03 20:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WpmResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wpm', models.IntegerField()),
                ('time', models.FloatField()),
                ('accuracy', models.FloatField()),
                ('user', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.text')),
            ],
            options={
                'verbose_name': 'WPM Result',
                'verbose_name_plural': 'WPM Results',
                'ordering': ['-created_at'],
            },
        ),
    ]
