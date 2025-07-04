from django.urls import path

from .views import CursorView, Home

urlpatterns = [
    path('', Home.as_view()),
    path('CursorView', CursorView.as_view()),
]