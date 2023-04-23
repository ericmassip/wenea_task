import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from chargepoints.api.serializers import ChargepointSerializer
from chargepoints.models import Chargepoint


class ChargepointList(generics.ListCreateAPIView):
    """List all charge points (including deleted ones), or create a new one."""

    queryset = Chargepoint.objects.all()
    serializer_class = ChargepointSerializer


class ChargepointDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or soft-delete a charge point. Note that deleted charge points cannot be updated, because
    they've been decommissioned and it doesn't make sense to update their status, nor to re-delete them because
    they're already deleted and it would mess up the deleted_at timestamp."""

    queryset = Chargepoint.objects.all()
    serializer_class = ChargepointSerializer

    def get_object(self):
        obj = super().get_object()

        if obj.is_deleted() and self.request.method in ["PUT", "DELETE"]:
            raise ValidationError(f"{obj.name} cannot be updated/deleted because it is already deleted")

        return obj

    def perform_update(self, serializer):
        old_status = self.get_object().status
        chargepoint = serializer.save()
        new_status = chargepoint.status

        if old_status != new_status:  # Only send notification if status has changed
            async_to_sync(get_channel_layer().group_send)(
                "lobby", {"type": "send_notification",
                          "message": f"{chargepoint.name} status is now '{chargepoint.get_status_display()}'"}
            )

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()

        async_to_sync(get_channel_layer().group_send)(
            "lobby",
            {"type": "send_notification", "message": f"{instance.name} has been deleted"}
        )
