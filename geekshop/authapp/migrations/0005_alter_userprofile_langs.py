# Generated by Django 3.2.6 on 2022-05-04 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_userprofile_langs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='langs',
            field=models.CharField(blank=True, default='RU', max_length=10, verbose_name='Язык'),
        ),
    ]
