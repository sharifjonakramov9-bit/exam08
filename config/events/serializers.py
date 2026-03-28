from rest_framework import serializers
from .models import Event, Registration


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

        # 1. Already registered?
        if Registration.objects.filter(user=user, event=event, status='registered').exists():
            raise serializers.ValidationError("Already registered")

        # 2. Capacity check
        registered_count = Registration.objects.filter(
            event=event, status='registered'
        ).count()

        if registered_count >= event.capacity:
            raise serializers.ValidationError("Event is full")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Registration.objects.create(user=user, **validated_data)