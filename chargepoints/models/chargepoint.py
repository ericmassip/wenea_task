from django.db import models


class Chargepoint(models.Model):
    class Status(models.TextChoices):
        READY = 'READY', 'ready'
        CHARGING = 'CHARGING', 'charging'
        WAITING = 'WAITING', 'waiting'
        ERROR = 'ERROR', 'error'

    name = models.CharField(max_length=32, unique=True)
    status = models.CharField(choices=Status.choices, default=Status.WAITING, max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def is_deleted(self):
        return self.deleted_at is not None

