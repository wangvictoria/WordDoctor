# Generated by Django 3.2.8 on 2022-02-08 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WordDoctorApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wordscape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wordscape_letters', models.CharField(max_length=10)),
                ('wordscape_length', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]