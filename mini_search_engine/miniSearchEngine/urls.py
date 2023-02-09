from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('textRecords/', views.textRecords, name='textRecords'),
    path('textRecords/details/<int:id>', views.details, name='details'),
    path('newRecord/', views.newRecord, name='newRecord'),
    path('recordAdded/<int:id>', views.recordAdded, name='recordAdded'),
    path('updateRecord/<int:id>', views.updateRecord, name='updateRecord'),
    path('searchResults/',views.searchResults, name='searchResults'),
    path('searchResults/<str:keyword>', views.searchResults, name='searchResults'),
    path('doesNotExist/', views.doesNotExist, name='doesNotExist')
]

handler404 = views.doesNotExist