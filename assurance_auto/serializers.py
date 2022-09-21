from rest_framework import serializers

from .models import Reglement, Contrat

class ContratSerializer(serializers.ModelSerializer):
   class Meta:
       model = Contrat
       fields = ('type_contrat', 'statut_assurance', 'vehicule','sous_couvert','categorie','active')

class ReglementSerializer(serializers.ModelSerializer):
   class Meta:
       model = Reglement
       fields = ('contrat', 'utilisateur','montant_a_regler', 'mode_de_paiment','regle')