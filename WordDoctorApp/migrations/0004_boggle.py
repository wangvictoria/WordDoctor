# Generated by Django 3.2.8 on 2022-03-15 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WordDoctorApp', '0003_wordle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boggle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boggle_11', models.CharField(max_length=1)),
                ('boggle_12', models.CharField(max_length=1)),
                ('boggle_13', models.CharField(max_length=1)),
                ('boggle_14', models.CharField(max_length=1)),
                ('boggle_21', models.CharField(max_length=1)),
                ('boggle_22', models.CharField(max_length=1)),
                ('boggle_23', models.CharField(max_length=1)),
                ('boggle_24', models.CharField(max_length=1)),
                ('boggle_31', models.CharField(max_length=1)),
                ('boggle_32', models.CharField(max_length=1)),
                ('boggle_33', models.CharField(max_length=1)),
                ('boggle_34', models.CharField(max_length=1)),
                ('boggle_41', models.CharField(max_length=1)),
                ('boggle_42', models.CharField(max_length=1)),
                ('boggle_43', models.CharField(max_length=1)),
                ('boggle_44', models.CharField(max_length=1)),
            ],
        ),
    ]
