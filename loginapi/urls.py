from django.urls import path
from django.urls import include
from .views import UserVerificationViewset

responsepdf=UserVerificationViewset.as_view({'post':'posting'})
urlpatterns = [
    path('/',responsepdf),
]