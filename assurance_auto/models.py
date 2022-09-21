from django.db import models
import uuid
import shortuuid
from decimal import *
from datetime import datetime, timedelta,date
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from simple_history.models import HistoricalRecords
import random
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms


class ProprietaireVehicule(models.Model):
    CIN = models.CharField(max_length=20, unique=True, blank=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero_permis = models.CharField(_('Numéro de permis'), max_length=15, null=True, blank=True)
    photo = models.ImageField(upload_to='Proprietaire/%Y/%m/%d', blank=True)
    adresse = models.TextField(max_length=100)
    telephone = models.CharField(max_length=16)
    email = models.EmailField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('-created',)
    def __str__(self):
        return self.CIN + ' ' + self.nom + ' ' + self.prenom

class Marque_Vehicule(models.Model):
    nom_marque = models.CharField(max_length=50, unique=True)
    class Meta:
        ordering=('nom_marque',)
    def __str__(self):
        return self.nom_marque

class Model_Vehicule(models.Model):
    nom_model = models.CharField(max_length=50, unique=True)
    marque = models.ForeignKey(Marque_Vehicule,on_delete=models.CASCADE)
    class Meta:
        ordering =('nom_model',)
    def __str__(self):
        return self.nom_model

class Vehicule(models.Model):
    type_fuel = (
        ('Essence','Essence'),
        ('Diesel','Diesel'),
       )
    immatriculation = models.CharField(_('Matricule'),max_length=20, db_index=True, unique=True)
    proprietaire = models.ForeignKey(ProprietaireVehicule, on_delete=models.CASCADE)
    model = models.ForeignKey(Model_Vehicule, on_delete=models.CASCADE)
    conducteur = models.CharField(_('Personne autorisée'),max_length=200, null=True, blank=True)
    permis = models.CharField(_('Numéro de permis'),max_length=50, null=True, blank=True)
    carroserie = models.CharField(max_length=50, null=True, blank=True)
    type_carburant = models.CharField(_('Energie'),max_length=15, choices=type_fuel)
    date_mise_en_circulation = models.DateField()
    puissance = models.CharField(max_length=20)
    poids_a_vide = models.CharField(max_length=10, blank=True)
    poids_autorise = models.CharField(max_length=10, null=True,blank=True)
    longueur = models.CharField(max_length=15, null=True, blank=True)
    largeur = models.CharField(max_length=15, null=True, blank=True)
    nb_place = models.IntegerField(null=True, blank=False)
    numero_carte_grise = models.CharField(max_length=20, blank=True, null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('-created',)
    def __str__(self):
        return self.immatriculation

# class Categorie_Contrat(models.Model):
#     nom = models.CharField(max_length=100, db_index=True)
#     # slug = models.SlugField(max_length=100, unique=True)
#     class Meta:
#         ordering = ('nom',)
#         verbose_name = 'categorie'
#         verbose_name_plural = 'categories'
#     def __str__(self):
#         return self.nom

class TypeContrat(models.Model):
    type_contrat_choices = (
        ('Responsabilité civile', 'RC'),
        ('Incendie du véhicule', 'IV'),
        ('Vol du véhicule', 'VV'),
        ('Brise de Glasses', 'BG'),
        ('Dommages Coalisions', 'DC'),
        ('Défense et Recours', 'DR'),
    )
    categorie_choices =(
        ('Tourisme', 'Tourisme'),
        ('Transport', 'Transport')
    )
    garantie = models.CharField(_('Type de garantie'), max_length=50, null=False, blank=False, choices=type_contrat_choices)
    duration = models.CharField(_('Durée (en nombre de jours)'), max_length=50, null=False, blank=False)
    montant_du_contrat = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=50, choices=categorie_choices, null=False, blank=False, default='Tourisme')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.garantie + ' ' + self.categorie +' ' + self.duration+ ' ' + ' jours'

class Contrat(models.Model):
    Statut_contrat = (
        ('Encours', 'Encours'),
        ('Suspendu', 'Suspendu'),
        ('Expiré', 'Expiré'),
    )
    
    # numero_de_contrat = shortuuid.uuid()
    type_contrat = models.ForeignKey(TypeContrat, on_delete=models.CASCADE, null=True, blank=False)
    tca = models.DecimalField(_('TCA 4%'),max_digits=10, decimal_places=2, default=0.00)
    numero_de_contrat = models.CharField(max_length=50, blank=True, null=True,db_index=True, unique=True)
    statut_assurance =models.CharField(max_length=15, choices=Statut_contrat, default='Non')
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_de_mois = models.IntegerField(null=True, blank=True)
    sous_couvert = models.CharField(_('S/C'),max_length=200, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    remainingdays=models.IntegerField(default=0)
    blocked_date=models.DateField()
    unblocked_date = models.DateField(null=True, blank=True)
    history = HistoricalRecords()
    class Meta:
        ordering=('-created',)
    @property
    def static_id(self):
        'C{0:07d}'.format(self.pk)

    def __str__(self):
        return str(self.numero_de_contrat)
        
    def save(self, *args, **kwargs):
        self.tca=self.type_contrat.montant_du_contrat*Decimal(0.04)
        if self.statut_assurance=="Suspendu":
            dt=abs(self.blocked_date-self.modified)
            # print('Difference est:',dt)
            numberOfDaysLeft= self.remainingdays-dt.days
            # print('Big diff',numberOfDaysLeft)
            self.remainingdays=numberOfDaysLeft
            self.blocked_date=date.today()
        super(Contrat, self).save(*args, **kwargs)

    def activeStatus(self):
        if self.nombre_de_mois==0:
            return self.active==False
        else:
            return self.active==True

    def get_NbDays(self):

        if self.statut_assurance=='Encours':
            
            # nb_Days = timedelta(days=self.remainingdays)+date.today()
            nb_Days = timedelta(days=self.remainingdays)+self.blocked_date
            return nb_Days
        elif self.statut_assurance=='Suspendu':
            nb_Days = timedelta(days=self.remainingdays) + self.blocked_date
            # jours=date(nb_Days)
            return nb_Days

        else:
            nb_Days = self.modified
            print(nb_Days)
            # print('Jours après blocage', nb_Days)
            return nb_Days

    def NewNumberOfDays(self):
        numberOfDays=timedelta(self.type_contrat.duration)-abs(date.today())
        print('Test 2',numberOfDays)
        return numberOfDays



class ContractManager(models.Manager):
    def ContractAmount(self, montant_du_contrat):
        return self.filter(montant_du_contrat=montant_du_contrat)

class Reglement(models.Model):
    payment_list = (('Espece', 'Espece'),
                    ('Cheque', 'Cheque'),
                    ('Huri money', 'Huri money'),
                    ('Holo', 'Holo'),
                    ('Mvola', 'Mvola'),
                    )
    code_reglement = models.CharField(max_length=50, blank=True, null=True, db_index=True, unique=True)
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reglement = models.DateField(auto_now_add=True)
    montant_a_regler = models.DecimalField(max_digits=10, decimal_places=2)
    mode_de_paiment = models.CharField(max_length=15,choices=payment_list)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    regle = models.BooleanField(default=False)
    history = HistoricalRecords()
    class Meta:
        ordering=('-created',)
    @property
    def static_id(self):
        'R{0:07d}'.format(self.pk)

    # def save(self, *args, **kwargs):
        last_record=Reglement.objects.latest('pk')
        # print(last_record.pk)
        # self.code_depense = random.randint(1000000, 9999999)
        # if self.pk != None:
        # self.code_reglement = 'R{0:07d}'.format(last_record.pk)
        # self.code_reglement='K{0:03d}'.format(last_record.pk+1)+\
        # '-'+ date.today().strftime("%m") +'A'+ date.today().strftime("%y")
        # super(Reglement, self).save(*args, **kwargs)

    def UpdatePaidAmount(self):
        amount=0
        totalAmount=amount+self.montant_a_regler
        return totalAmount

    def __str__(self):
        return str(self.code_reglement)


class ReglementContrat(models.Model):
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE)
    reglement = models.ForeignKey(Reglement, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return '{}'.format(self.id)

    def getTotalPaid(self):
        amountPaid=0
        contratList = Contrat.objects.all()
        for contratLine in contratList:
            if contratLine.numero_de_contrat==self.contrat:
                amountPaid=amountPaid+self.montant
        # print(amountPaid)
        return amountPaid

class ContratHistory(models.Model):
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE)
    created = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)



# def update_Contract(numero_de_contrat, date, categorie, propietaire, montant):
#     contrat, created = Contrat.objects.get_or_create(numero_de_contrat=numero_de_contrat)
#     contrat.date_contrat=date
#     contrat.categorie=categorie
#     contrat.vehicule=propietaire
#     contrat.montant_du_contrat=montant
#     contrat.save()
#     contract_history, created=ContratHistory.objects.get_or_create(
#         contrat=contrat, created=datetime.date.today()
#     )
#     contract_history.montant
#     contract_history.save()

class Accidents(models.Model):
    Vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    concerne_vehicule = models.CharField(_('Immatriculation'), max_length=50, help_text='Numéro de la voiture qui a fait l\'accident. ')
    assureur = models.CharField(max_length=250, null=True, blank=True)
    date_accident = models.DateField(_('Date de l\'accident'))
    lieu_accident = models.CharField(max_length=500, null=False, blank=False)
    # conducteur = models.TextChoices()
    causes = models.TextField(_('Quelles sont les causes de l\'accident?'))
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.Vehicule.immatriculation)

class Reparations(models.Model):
    reparation_choices =(
        ('Oui','Oui'),
        ('Non','Non')
    )
    id_accident = models.ForeignKey(Accidents, on_delete=models.CASCADE)
    garagiste = models.CharField(max_length=200, null=False, blank=False)
    adresse = models.CharField(max_length=250, null=False, blank=False)
    vehicule_repare = models.CharField(_('Les réparations sont elles finies?'), max_length=5, choices=reparation_choices)
    commentaires = models.TextField()


class Depenses(models.Model):
    code_depense = models.CharField(max_length=10, blank=True, null=True, db_index=True)
    objet = models.CharField(max_length=200, null=False, blank=False)
    beneficiaire = models.CharField(_('Bénéficiaire'), max_length=500, null=False, blank=False)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_depense = models.DateField()
    commentaires = models.TextField(null=True, blank=True)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    @property
    def static_id(self):
        'C{0:07d}'.format(self.pk)

    def __str__(self):

        return str(self.code_depense)

    def save(self, *args, **kwargs):
        # self.code_depense = random.randint(1000000, 9999999)
        if self.pk != None:
            self.code_depense = 'D{0:07d}'.format(self.pk)
        super(Depenses, self).save(*args, **kwargs)


