# Generated by Django 3.1.3 on 2022-03-03 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assurance_auto', '0010_auto_20220310_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proprietairevehicule',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]
