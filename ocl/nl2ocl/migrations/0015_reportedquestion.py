# Generated by Django 4.0.5 on 2022-07-22 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nl2ocl', '0014_alter_ocltranslation_options_nlquestion_approved_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reasson', models.TextField(default=None)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('nlquestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportedQuestion', to='nl2ocl.nlquestion')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]