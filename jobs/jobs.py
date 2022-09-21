from assurance_auto.models import Contrat
from datetime import datetime, timedelta,date
from django.conf import settings

def status_schedule(): 
	contractList = Contrat.objects.all()
	for contrat in contractList:
		if contrat.get_NbDays() <= date.today():
			Contrat.objects.filter(id=contrat.id).update(statut_assurance='Expiré')
			contrat.statut_assurance = 'Expiré'
			# print('Numéro de contrat est :',contrat.numero_de_contrat,\
				# ' et le statut est: ',contrat.statut_assurance)
			