from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings

from .models import Match

def match_reminder():
    date_today = date.today()
    qs = Match.objects.filter(reminder_emails=False)

    for match in qs:
        if match.match_date - timedelta(days=1) == date_today:
            match_players = match.players.all()
            for player in match_players:
                subject = 'Match reminder'
                message = f'Przypomnienie o nadchodzącym meczu {match.name}, dnia {match.match_date}, o godzinie {match.match_time}'
                email_from = settings.EMAIL_HOST_USER
                email_to = [player.email]
                send_mail(subject, message, email_from, email_to)

            match.reminder_emails = True
            match.save()
      
        