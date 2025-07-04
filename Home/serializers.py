from rest_framework import serializers
from .models import Cursor
from django.contrib.auth import get_user_model

User = get_user_model()


class CursorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Cursor
        fields  = "__all__"