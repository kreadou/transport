# Generated by Django 3.2.6 on 2022-09-22 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100, unique=True, verbose_name='profession')),
            ],
            options={
                'ordering': ('libelle',),
            },
        ),
    ]
