from rest_framework import serializers
from powerball_checker.bobgtw import BobGateway
from powerball_checker.models import Ticket, Prize
from django.http import Http404


class PrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = ('draw_date', )


class TicketSerializer(serializers.Serializer):
    draw_date = serializers.DateField()
    ticket = serializers.JSONField()

    def winner(self):
        """
        If the object is stored, return this value.

        if not, search on the backend and updates the local object
        """
        ticket = Ticket.objects.filter(
            prize__draw_date=self.validated_data["draw_date"],
            numbers=self.validated_data["ticket"]
        )
        if not ticket:
            raise Http404()

        # not hadling duplicate ones
        ticket = ticket[len(ticket) - 1]

        if ticket.drawed():
            return ticket.winning
        else:
            iswinner = BobGateway().is_a_winner_ticket(
                self.validated_data["draw_date"].strftime('%Y-%m-%d'),
                self.validated_data["ticket"],
            )
            ticket.winning = iswinner
            ticket.save()

            return iswinner

    def save(self):
        tkt = BobGateway().create_ticket(
            self.validated_data["draw_date"].strftime('%Y-%m-%d'),
            self.validated_data["ticket"],
        )

        prize, created = Prize.objects.get_or_create(
            draw_date=self.validated_data["draw_date"],
        )
        if created:
            prize.code = tkt['prize_code']
            prize.save()

        ticket = Ticket(
            prize=prize,
            code=tkt['ticket_code'],
            numbers=self.validated_data["ticket"],
            winning=None
        )
        ticket.save()
