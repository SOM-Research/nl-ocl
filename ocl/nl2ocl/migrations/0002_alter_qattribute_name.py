# Generated by Django 4.0.5 on 2022-07-04 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nl2ocl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qattribute',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]