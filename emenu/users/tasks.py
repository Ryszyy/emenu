import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from config import celery_app
from emenu.cards.models import Card

User = get_user_model()


def create_email_body(created, updated):
    body = "Greetings \n"
    if not created:
        body += f'New Cards {created}\n'
    else:
        body += 'No new cards added\n'
    if not updated:
        body += f'Updated cards {updated}\n'
    else:
        body += 'No updated\n'
    body += "Cheers"
    return body


@celery_app.task
def send_mail_to_users():
    users_emails = User.objects.values_list("email", flat=True)
    yesterday = timezone.now().today() - timezone.timedelta(days=1)
    yesterday = yesterday.replace(tzinfo=pytz.UTC)
    new_cards = Card.objects.filter(add_date__date=yesterday)
    updated_cards_vals = Card.objects.filter(
        updated__date=yesterday).exclude(
        id__in=new_cards).values_list(
        "name", flat=True)
    new_cards_vals = new_cards.values_list("name", flat=True)
    body = create_email_body(new_cards_vals, updated_cards_vals)

    for email in users_emails:
        send_mail(
            'Card News',
            body,
            settings.ADMINS[0][1],
            [email],
            fail_silently=False,
        )
