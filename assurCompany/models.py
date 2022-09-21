from operator import mod
from django.db import models
from django.utils.translation import ugettext_lazy as _
from decimal import Decimal
# Create your models here.

# class Category(models.Model):
#     category_choice = (
#         (1,'5%')
#         (2, '10%'),
#         (3, '15%'),
#         (4, '20%'),
#         (5, '25%'),
#         (6, '30%'),
#         (7, '35%'),
#         (8, '40%'),
#         (9, '45%'),
#         (10, '50%'),
#         (11, '55%'),
#         (12, '60%'),
#         (13, '65%'),
#         (14, '70%'),
#         (15, '75%'),
#         (16, '80%'),
#         (17, '85%'),
#         (18, '90%'),
#         (19, '95%'),
#         (20, '100%'),
#     )
#     categorie = models.CharField(max_length=5, choices=category_choice)
    

class Companies(models.Model):
    category_choice = (
        (1,'5%'),
        (2, '10%'),
        (3, '15%'),
        (4, '20%'),
        (5, '25%'),
        (6, '30%'),
        (7, '35%'),
        (8, '40%'),
        (9, '45%'),
        (10, '50%'),
        (11, '55%'),
        (12, '60%'),
        (13, '65%'),
        (14, '70%'),
        (15, '75%'),
        (16, '80%'),
        (17, '85%'),
        (18, '90%'),
        (19, '95%'),
        (20, '100%'),
    )
    categorie = models.CharField(max_length=5, choices=category_choice)
    ID_Company = models.CharField(_('Régistre de commerce'),max_length=50, null=False, blank=False)
    name_comapany = models.CharField(_('Nom de la Société'), max_length=300, null=False, blank=False)
    adresse_company = models.TextField('Adresse')
    def __str__(self) -> str:
        return super().__str__(self.ID_Company + ' '+ self.name_comapany)

class Employees(models.Model):
    matrimoniale_choices=(
        ('marié(e)','marié(e)'),
        ('célibataire','célibataire'),
        ('divorcé(e)','divorcé(e)'),
        ('Veuf(ve)','Veuf(ve)'),
    )
    compagnie = models.ForeignKey(Companies, on_delete=models.CASCADE)
    ID_empl = models.CharField(max_length=50, null=False, blank=False)
    CIN = models.CharField(max_length=20, null=False, blank=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naiss=models.DateField()
    photo = models.ImageField(upload_to='Employés/%Y/%m/%d', blank=True)
    adresse = models.TextField(max_length=100)
    telephone = models.CharField(max_length=16)
    email = models.EmailField(max_length=100)
    sit_matrimoniale=models.CharField(_('Situation matrimoniale'),max_length=20, choices=matrimoniale_choices)
    nb_enfant = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('created',)
    def __str__(self):
        return self.CIN + ' ' + self.nom + ' ' + self.prenom


class Hospitals(models.Model):
    ID_Hospital = models.CharField(_('Régistre de commerce'),max_length=50, null=False, blank=False)
    name_hospital = models.CharField(_('Hôpital/Pharmacie'), max_length=300, null=False, blank=False)
    docteur = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self) -> str:
        return self.ID_Hospital + ' '+ self.name_hospital

class Consultations(models.Model):
    employe = models.ForeignKey(Employees, on_delete=models.CASCADE)
    hopital = models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    medecin = models.CharField(max_length=250, null=True, blank=True)
    date_consultation = models.DateField()
    amount_to_pay = models.DecimalField(_('Frais de consultation'),max_digits=6, decimal_places=2)
    Ordonnace = models.ImageField(upload_to='Ordonnaces/%Y/%m/%d', blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    @property
    def static_id(self):
        'C{0:07d}'.format(self.pk)


class Remboursement(models.Model):
    consultation = models.ForeignKey(Consultations, on_delete=models.CASCADE)
    Facture = models.ImageField(upload_to='Fact_Reglement/%Y/%m/%d', blank=False, null=False)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    regle = models.BooleanField(_('Réglé'),default=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    @property
    def static_id(self):
        'C{0:07d}'.format(self.pk)

    def save(self, montant=Decimal('0.0'), *args, **kwargs):
        self.montant = self.consultation.employe.compagnie.categorie
        
        super(Remboursement, self).save(*args, **kwargs)

    