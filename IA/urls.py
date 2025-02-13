from django.urls import path
from .views import obter_insights

urlpatterns = [
    path('insights/', obter_insights, name='obter_insights'),
]
