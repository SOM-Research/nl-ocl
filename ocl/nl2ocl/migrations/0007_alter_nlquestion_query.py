# Generated by Django 4.0.5 on 2022-07-04 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nl2ocl', '0006_remove_qclass_source_qmodel_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nlquestion',
            name='query',
            field=models.TextField(default=None, null=True),
        ),
    ]
