# Generated by Django 4.0.5 on 2022-07-04 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nl2ocl', '0003_alter_nlquestion_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qclass',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
