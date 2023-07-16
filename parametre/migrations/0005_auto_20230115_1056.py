# Generated by Django 3.2.6 on 2023-01-15 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametre', '0004_auto_20221031_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='devis',
            name='ligne_bon_devis',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Remplacer vos références'),
        ),
        migrations.AddField(
            model_name='devis',
            name='utiliser_ligne_bon_devis',
            field=models.BooleanField(blank=True, default=False, verbose_name='Je voudrais remplacer vos références'),
        ),
    ]
