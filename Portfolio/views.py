from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from DjangoSonion.DRF import AnonymousPermissionOnly, isAdminOrPostOnly

from .models import Skill, Project, CMessage, Certificate, Info, Use, SocialMedia
from .serializers import (
    SkillsModelSerializer, ProjectsModelSerializer, MessagesModelSerializer, 
    CertificateModelSerializer, InfoModelSerializer, UseModelSerializer, 
    SocialMediaModelSerializer
)
# Create your views here.

class ListSkillsANDTools(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillsModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class SkillDetailView(generics.RetrieveAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillsModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ListProjects(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class Message(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = CMessage.objects.all()
    serializer_class = MessagesModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class Messages(generics.ListCreateAPIView):
    permission_classes = [isAdminOrPostOnly]
    queryset = CMessage.objects.all()
    serializer_class = MessagesModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CertificatesView(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class CertificateDetailView(generics.RetrieveAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class InfoView(generics.ListAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class InfoDetailView(generics.RetrieveAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class UseView(generics.ListAPIView):
    queryset = Use.objects.all()
    serializer_class = UseModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class UseDetailView(generics.RetrieveAPIView):
    queryset = Use.objects.all()
    serializer_class = UseModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class SocialMediaView(generics.ListAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class SocialMediaDetailView(generics.RetrieveAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)