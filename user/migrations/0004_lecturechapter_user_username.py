# Generated by Django 5.0.2 on 2024-03-17 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_lecturechapter_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturechapter',
            name='user_username',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
