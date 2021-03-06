# Generated by Django 3.2.8 on 2022-02-15 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WordDoctorApp', '0002_wordscape'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wordle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wordle_loc1', models.CharField(blank=True, max_length=1, null=True)),
                ('wordle_loc2', models.CharField(blank=True, max_length=1, null=True)),
                ('wordle_loc3', models.CharField(blank=True, max_length=1, null=True)),
                ('wordle_loc4', models.CharField(blank=True, max_length=1, null=True)),
                ('wordle_loc5', models.CharField(blank=True, max_length=1, null=True)),
                ('wordle_known_letters', models.CharField(blank=True, max_length=5, null=True)),
                ('wordle_invalid_letters', models.CharField(blank=True, max_length=26, null=True)),
            ],
        ),
    ]
