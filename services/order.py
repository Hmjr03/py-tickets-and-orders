from django.db import transaction
from django.utils.dateparse import parse_datetime

from db.models import Order
from db.models import Ticket
from db.models import User


@transaction.atomic
def create_order(
    tickets,
    username,
    date=None
):
    user = User.objects.get(
        username=username
    )

    order = Order.objects.create(
        user=user
    )

    if date:
        order.created_at = parse_datetime(date)
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data[
                "movie_session"
            ],
            order=order
        )

    return order


def get_orders(username=None):
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(
            user__username=username
        )

    return queryset
