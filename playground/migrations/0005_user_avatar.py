# Generated by Django 4.1.7 on 2023-05-24 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0004_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
    ]
