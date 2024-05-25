from rest_framework import serializers
from .models import Weekly


class WeeklySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekly
        fields = (
            "username",
            "lang",
        ) 
