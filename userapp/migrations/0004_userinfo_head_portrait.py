# Generated by Django 4.0.3 on 2022-04-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_alter_area_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='head_portrait',
            field=models.ImageField(default='tx.png', upload_to=''),
        ),
    ]