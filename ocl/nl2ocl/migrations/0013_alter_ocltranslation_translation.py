# Generated by Django 4.0.5 on 2022-07-09 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nl2ocl', '0012_ocltranslation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocltranslation',
            name='translation',
            field=models.TextField(default=None),
        ),
    ]
