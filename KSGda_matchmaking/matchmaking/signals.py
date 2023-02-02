from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Player

def player_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='player')
		instance.groups.add(group)
		Player.objects.create(
                user=instance,
                name=instance.username,
            )
		print('Profile created!')

post_save.connect(player_profile, sender=User)