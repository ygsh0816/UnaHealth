from django.urls import path
from . import views

urlpatterns = [
    path('levels/', views.GlucoseLevelList.as_view(), name='glucoselevel-list'),
    path('levels/<int:pk>/', views.GlucoseLevelDetail.as_view(), name='glucoselevel-detail'),
    path('levels/create/', views.GlucoseLevelCreate.as_view(), name='glucoselevel-create'),
    path('levels/export/', views.GlucoseLevelExport.as_view(), name='glucoselevel-export'),
]
