# Generated by Django 2.2 on 2019-04-30 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='about_me',
            field=models.TextField(max_length=140, null=True, verbose_name='About me'),
        ),
    ]