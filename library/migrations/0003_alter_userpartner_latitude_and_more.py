# Generated by Django 4.0.3 on 2022-03-15 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_userpartner_latitude_userpartner_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpartner',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=11, null=True),
        ),
        migrations.AlterField(
            model_name='userpartner',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=11, null=True),
        ),
    ]
