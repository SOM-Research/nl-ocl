# Generated by Django 4.0.5 on 2022-07-04 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nl2ocl', '0004_alter_qclass_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='nlquestion',
            name='query',
            field=models.TextField(default=None),
        ),
    ]
