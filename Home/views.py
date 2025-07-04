from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from DjangoSonion.DRF import AnonymousPermissionOnly
from rest_framework.views import APIView

from .models import Cursor
from .serializers import CursorModelSerializer
# Create your views here.

class CursorView(generics.ListAPIView):
    serializer_class = CursorModelSerializer
    queryset = Cursor.objects.all()

    def get(self, request):
        return self.list(request)


class Home(APIView):

    def get(self, request):
        return Response({'home': 'empty'})