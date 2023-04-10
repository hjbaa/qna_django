# Generated by Django 4.2 on 2023-04-10 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme_app', '0003_alter_profile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='askme_app.tag'),
        ),
    ]
