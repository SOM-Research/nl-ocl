# Generated by Django 4.0.5 on 2022-07-07 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nl2ocl', '0010_rename_rol_qassociate_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qassociate',
            name='role',
            field=models.CharField(choices=[('FK', 'FK'), ('RV', 'RV')], default='FK', max_length=2),
        ),
    ]
