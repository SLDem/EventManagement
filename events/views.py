from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer

from django.core.mail import send_mail
from django.conf import settings


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'location']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='register')
    def register_for_event(self, request, pk):
        event = Event.objects.get(pk=pk)
        user = request.user

        if EventRegistration.objects.filter(event=event, user=user).exists():
            return Response({"detail": "User already registered for this event."}, status=400)

        EventRegistration.objects.create(event=event, user=user)
        return Response({"detail": "Successfully registered for the event."}, status=201)

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        user = self.request.user
        serializer.save(user=user)

        # Send registration confirmation email
        try:
            send_mail(
                subject=f"Confirmation: {event.title} Registration",
                message=f"Hello {user.username},\n\nYou have successfully registered for {event.title}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            print('sent email success')
        except:
            print('not sent email')
