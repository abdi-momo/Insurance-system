from django import forms
from assurance_auto.models import ProprietaireVehicule,Reglement,\
Vehicule,Contrat,Marque_Vehicule,Model_Vehicule, TypeContrat, Depenses

from django.contrib.auth.models import User

class ProprietaireAddForm(forms.ModelForm):
    class Meta:
        model= ProprietaireVehicule
        fields=['CIN','nom','prenom','photo','adresse','telephone','email']
        # widgets={
        #     'CIN':forms.TextInput(attrs={'class':'input'}),
        # }

class DepenseAddForm(forms.ModelForm):
    class Meta:
        model=Depenses
        exclude=('code_depense','utilisateur',)

class MarqueAddForm(forms.ModelForm):
    class Meta:
        model=Marque_Vehicule
        fields='__all__'

class ModelAddForm(forms.ModelForm):
    class Meta:
        model=Model_Vehicule
        fields='__all__'

class VehiculeAddForm(forms.ModelForm):
    class Meta:
        model=Vehicule
        fields='__all__'

class ContratAddFrom(forms.ModelForm):
    class Meta:
        model=Contrat
        exclude=('utilisateur','nombre_de_mois','numero_de_contrat','remainingdays','blocked_date','unblocked_date','montant_regle', 'tca',)
        # fields=('Categorie_assurance','Proprietaire','Conducteur','periode_jours','montant_du_contrat','statut',)

class TypeContratAddForm(forms.ModelForm):
    class Meta:
        model=TypeContrat
        exclude=('utilisateur',)

class ReglementAddForm(forms.ModelForm):
    class Meta:
        model=Reglement
        exclude = ('utilisateur','remainAmount','code_reglement')
        # fields='__all__'
        widgets = {
               'mode_de_paiment': forms.RadioSelect()
           }