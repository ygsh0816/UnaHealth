from django.urls import path
from . import views

urlpatterns = [
    path('levels/', views.GlucoseLevelList.as_view(), name='glucoselevel-list'),
    path('levels/<int:pk>/', views.GlucoseLevelDetail.as_view(), name='glucoselevel-detail'),
]
