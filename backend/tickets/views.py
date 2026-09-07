from rest_framework import generics, permissions

from .models import Ticket
from .serializers import TicketSerializer

def get_visible_tickets(user):
    if user.is_superuser or user.groups.filter(name="ADMIN").exists():
        return Ticket.objects.all()

    if user.groups.filter(name="CUSTOMER").exists():
        return Ticket.objects.filter(created_by=user)

    return Ticket.objects.none()


class TicketListCreateView(generics.ListCreateAPIView):
    
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_visible_tickets(self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_visible_tickets(self.request.user)