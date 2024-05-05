# Generated by Django 5.0.3 on 2024-04-30 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controltower', '0002_datapoint'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='SavedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('text', models.TextField()),
                ('button_choice', models.CharField(max_length=100)),
                ('images', models.ManyToManyField(blank=True, to='controltower.image')),
            ],
        ),
    ]