# Generated by Django 4.1.7 on 2023-06-23 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0005_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='images',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]