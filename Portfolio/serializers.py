from rest_framework import serializers
from .models import Skill, Project, CMessage, Certificate, Info, Use, SocialMedia

class SkillsModelSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model   = Skill
        fields  = [
            'id', 'title', 'about', 'summary', 'icon', 'uses', 'abilites', 'kind', 'section', 'yearsOfExprience', 'progress'
        ]

    def get_icon(self, obj):
        if obj.icon:
            return obj.icon.url if hasattr(obj.icon, 'url') else None
        return obj.icon_url

class ProjectsModelSerializer(serializers.ModelSerializer):
    stack = SkillsModelSerializer(many=True, read_only=True)
    
    class Meta:
        model   = Project
        fields  = "__all__"

class MessagesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model   = CMessage
        fields  = "__all__"

class CertificateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"

class InfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = "__all__"

class UseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Use
        fields = "__all__"

class SocialMediaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"