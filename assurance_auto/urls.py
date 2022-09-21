from django.urls import path, include
from . import views
from rest_framework import routers
from assurance_auto.views import ContratViewSet,ReglementViewSet


router = routers.DefaultRouter()
router.register(r'contrat', ContratViewSet)
router.register(r'reglement', ReglementViewSet)


app_name='assurance_auto'
urlpatterns=[
    path('', views.home_page,name='home_page'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('add/proprietaire/', views.AddClient, name='addProprietaire'),
    path('client/', views.Clients, name='clients'),
    path('ListeClient/', views.ClientList, name='ListeClient'),
    path('client/<int:id>/edit',views.ClientUpdate, name='Edit_Client'),

    path('marque/',views.CreateMarque, name='AddMarque'),
    path('marque/List',views.MarqueList, name='MarqueListe'),
    path('<int:id>/edit',views.UpdateMarque, name='Edit_Marque'),

    path('model/',views.CreateModel, name='AddModel'),
    path('model/List',views.ModelListe, name='Model_Liste'),

    path('vehicule/',views.CreateVehicule, name='AddVehicule'),
    path('vehicule/List/',views.VehiculeListe, name='Vehicule_Liste'),
    path('vehicule/<int:id>/edit',views.VehiculeUpdate, name='Edit_Vehicule'),
    path('Vehicule/<int:id>/detail/',views.vehicule_detail, name='Detail_vehicule'),

    path('typeContrat/Assurance/',views.CreateContratType, name='TypeContrat_Assurance'),
    path('type_contrat/<int:id>/edit',views.ContratTypeUpdate, name='Edit_typeContrat'),
    path('vehicule/add',views.CreateContrat, name='AddContrat'),
    path('contrat/List/',views.ContratListe, name='Contrat_Liste'),
    path('contrat/<int:id>/edit',views.ContratUpdate, name='Edit_Contrat'),
    path('contrat/<int:id>/modif',views.ModifContrat, name='Modif_Contrat'),
    path('contrat/<int:id>/detail/',views.ContractDetail, name='Detail_contrat'),

    path('reglement/nouveau/', views.new_invoice, name='new_invoice'),
    path('nouveau/Reglement/',views.AddReglement, name='addReglement'),
    # path('nouveau/Reglement/',views.CreateReglement, name='addReglement'),
    path('reglement/<int:id>/edit/',views.UpdateReglement, name='Edit_Reglement'),
    path('reglement/<int:id>/edit/',views.UpdateReglement, name='Edit_Reglement'),
    path('reglement/<int:id>/modify/',views.ModifyReglement, name='Modify_Reglement'),
    path('reglement/<int:id>/detail/',views.detailReglement, name='DetailReglement'),
    path('reglement/<int:id>/pdf/', views.order_pdf, name='reglement_pdf'),


     path('nouvelle/Depense/',views.CreateDepenses, name='nouvelleDepense'),
     path('depense/<int:id>/details/',views.DepenseDetail, name='detail_Depense'),
     path('depense/<int:id>/modif',views.ModifDepense, name='Modif_Depense'),
    

    # Contrat assurance
    path('assurance/alerte/', views.notification, name='alerte_expiration'),
    path('assurance/<int:id>/carton/', views.Carton_assurance, name='carton_assurance'),



    path('', include(router.urls)),

]