# Generated by Django 5.0.6 on 2024-06-29 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bicycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('available', 'Available'), ('rented', 'Rented')], default='available', max_length=10)),
            ],
        ),
    ]
