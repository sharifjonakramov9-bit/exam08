from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


class Event(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'

    EVENT_TYPE_CHOICES = [
        (ONLINE, 'Online'),
        (OFFLINE, 'Offline'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES)
    location = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError("End time cannot be earlier than start time")

        if self.event_type == self.OFFLINE and not self.location:
            raise ValidationError("Offline events must have location")

    def __str__(self):
        return self.title
    

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


class Event(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'

    EVENT_TYPE_CHOICES = [
        (ONLINE, 'Online'),
        (OFFLINE, 'Offline'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES)
    location = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError("End time cannot be earlier than start time")

        if self.event_type == self.OFFLINE and not self.location:
            raise ValidationError("Offline events must have location")

    def __str__(self):
        return self.title



class Registration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'event']

    def __str__(self):
        return f"{self.user} - {self.event}"