from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Player(models.Model):
    POSITION = (
        ('Bramkarz', 'Bramkarz'),
        ('Obrońca', 'Obrońca'),
        ('Pomocnik', 'Pomocnik'),
        ('Napastnik', 'Napastnik'),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField("Imię/nazwisko",max_length=200, null=True)
    nickname = models.CharField("Ksywka",max_length=200, null=True)
    favorite_position = models.CharField("Ulubiona pozycja",max_length=200, null=True, choices=POSITION)
    phone = models.CharField("Nr telefonu",max_length=200, null=True)
    email = models.CharField("Email",max_length=200, null=True)
    yellow_cards = models.IntegerField("Żółte kartki", default=0,null=True)
    red_cards = models.IntegerField("Czerwone kartki", default=0,null=True)
    ticket_counter = models.IntegerField("Zgłoszenia", default=0,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    superuser = models.BooleanField(default=False, null=True)

    def __str__(self) -> str:
        return str(self.name)

class Promoter(models.Model):
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField("Imię/nazwisko",max_length=200, null=True)
    phone = models.CharField("Nr telefonu", max_length=200, null=True)
    email = models.CharField("Email", max_length=200, null=True)
    player = models.OneToOneField(Player, null=True, blank=True, on_delete=models.CASCADE,)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.name

class Match(models.Model):
    SKILL_LEVEL = (
        ('Początkujący', 'Początkujący'),
        ('Zaawansowany', 'Zaawansowany'),
        ('Pro', 'Pro'),
    )
    name = models.CharField("Nazwa spotania",max_length=200, null=True)
    skill_level = models.CharField("Poziom umiejętności", max_length=200, null=True, choices=SKILL_LEVEL)
    reserved_slots = models.IntegerField("Zarezerwowane miejsca", default= 0, null=True)
    slots = models.IntegerField("Ilośc miejsc",null=True)
    match_cost = models.IntegerField("Koszt meczu", default=0,null=True)
    match_result = models.CharField("Wynik spotania", default="0 - 0", max_length=200, null=True)
    localization = models.CharField("Lokalizacja",max_length=200, null=True)
    match_date = models.DateField("Data spotkania", null=True,)
    match_time = models.TimeField("Czas spotkania", null=True,)
    promoter = models.ForeignKey(Promoter, null=True, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    reminder_emails = models.BooleanField(default=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.name}"

class ReservesPlayer(models.Model):
    match_id = models.ForeignKey(Match, null=True, on_delete=models.CASCADE)
    player_id = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.match_id.name} - {self.player_id.name}"

class Reserves(models.Model):
    match_id = models.ForeignKey(Match, null=True, on_delete=models.CASCADE)
    players = models.ManyToManyField(ReservesPlayer)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.match_id.name}"

class PlayerRating(models.Model):
    match_id = models.ForeignKey(Match, null=True, on_delete=models.CASCADE)
    player_id = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    rate = models.FloatField("Ocena", max_length=200, null=True,)

    def __str__(self) -> str:
        return f"{self.match_id.name} - {self.player_id.name}"

class MatchPlayersRating(models.Model):
    match_id = models.ForeignKey(Match, null=True, on_delete=models.CASCADE)
    rated_players = models.ManyToManyField(PlayerRating)   

    def __str__(self) -> str:
        return f"{self.match_id.name}"

class PlayerMatchRateDone(models.Model):
    player_id = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE,)
    match_players_rating_id = models.ForeignKey(MatchPlayersRating, null=True, blank=True, on_delete=models.CASCADE,)
    rate_done = models.BooleanField(default=False, null=True)

class Comments(models.Model):
    match_id = models.ForeignKey(Match, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return '%s - %s' % (self.match_id.name, self.user)

class Ticket(models.Model):
    TICKET_TITLE = (
        ('Czerwona kartka', 'Czerwona kartka'),
        ('Dostęp do organizowania meczy', 'Dostęp do organizowania meczy'),
    )
    player_id = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    title = models.CharField("Tytuł", max_length=200, null=True, choices=TICKET_TITLE)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.player_id} - {self.title}"