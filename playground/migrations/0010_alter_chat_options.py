# Generated by Django 4.0.3 on 2024-08-13 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0009_chat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['-created']},
        ),
    ]