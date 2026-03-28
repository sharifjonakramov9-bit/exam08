from rest_framework import generics
from .models import Registration
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer

class RegisterView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]
    