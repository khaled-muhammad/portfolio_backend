from django.urls import path

from .views import (
    ListSkillsANDTools, SkillDetailView, ListProjects, ProjectDetailView, 
    Messages, Message, CertificatesView, CertificateDetailView,
    InfoView, InfoDetailView, UseView, UseDetailView,
    SocialMediaView, SocialMediaDetailView
)

urlpatterns = [
    # Skills
    path('ST/', ListSkillsANDTools.as_view()),
    path('ST/<pk>/', SkillDetailView.as_view()),
    
    # Works
    path('projects/', ListProjects.as_view()),
    path('projects/<pk>/', ProjectDetailView.as_view()),
    
    # Certificates
    path('certificates/', CertificatesView.as_view()),
    path('certificates/<pk>/', CertificateDetailView.as_view()),
    
    # Info
    path('info/', InfoView.as_view()),
    path('info/<pk>/', InfoDetailView.as_view()),
    
    # Uses
    path('uses/', UseView.as_view()),
    path('uses/<pk>/', UseDetailView.as_view()),
    
    # Social Media
    path('social-media/', SocialMediaView.as_view()),
    path('social-media/<pk>/', SocialMediaDetailView.as_view()),
    
    # Messages
    path('messages/', Messages.as_view()),
    path('messages/<pk>/', Message.as_view()),
]