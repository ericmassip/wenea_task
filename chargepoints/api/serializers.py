from rest_framework import serializers

from chargepoints.models import Chargepoint


class ChargepointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chargepoint
        fields = ('id', 'name', 'status', 'created_at', 'deleted_at')
        read_only_fields = ('id', 'created_at', 'deleted_at')
