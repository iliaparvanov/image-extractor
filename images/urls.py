from django.urls import path
from .views import ListImage, DetailImage

urlpatterns = [
    path('<int:pk>/', DetailImage.as_view(), name='image-detail'),
    path('', ListImage.as_view()),
]