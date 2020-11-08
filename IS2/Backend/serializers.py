from rest_framework import serializers
from .models import *


class ClienteSerialize(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
