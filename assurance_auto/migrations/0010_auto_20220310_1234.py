# Generated by Django 3.1.3 on 2022-03-10 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assurance_auto', '0009_auto_20220228_0115'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contrat',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='proprietairevehicule',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='reglement',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='contrat',
            name='blocked_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='statut_assurance',
            field=models.CharField(choices=[('Encours', 'Encours'), ('Suspendu', 'Suspendu'), ('Expiré', 'Expiré')], default='Non', max_length=15),
        ),
        migrations.AlterField(
            model_name='historicalcontrat',
            name='blocked_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='historicalcontrat',
            name='statut_assurance',
            field=models.CharField(choices=[('Encours', 'Encours'), ('Suspendu', 'Suspendu'), ('Expiré', 'Expiré')], default='Non', max_length=15),
        ),
    ]