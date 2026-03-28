from rest_framework import serializers
from .models import Event, Registration
from django.db import transaction

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['user', 'status']

    def validate(self, data):
        user = self.context['request'].user
        event = data['event']

        if Registration.objects.filter(user=user, event=event, status='registered').exists():
            raise serializers.ValidationError("Already registered")

        registered_count = Registration.objects.filter(
            event=event, status='registered'
        ).count()

        if registered_count >= event.capacity:
            raise serializers.ValidationError("Event is full")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Registration.objects.create(user=user, **validated_data)
    


def create(self, validated_data):
    user = self.context['request'].user
    event = validated_data['event']

    with transaction.atomic():
        registered_count = Registration.objects.select_for_update().filter(
            event=event, status='registered'
        ).count()

        if registered_count >= event.capacity:
            raise serializers.ValidationError("Event is full")

        return Registration.objects.create(user=user, **validated_data)
    

def validate(self, data):
    if data['end_time'] < data['start_time']:
        raise serializers.ValidationError("End time must be after start time")
    return data