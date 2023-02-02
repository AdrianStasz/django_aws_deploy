import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime, date

from .models import *
from .forms import *
from .tokens import account_activation_token
from .actions import searching_for_next_matches, match_history
from .decorators import unauthenticated_user, check_promoter


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Aktywacja maila zakończona pomyślnie, teraz możesz się zalogować")
        return redirect('login')
    else:
        messages.error(request, "Link aktywacyjny jest nieprawidłowy!")
        
    return redirect('login')

def activateEmail(request, user, to_email):
    mail_subject = 'Aktywacja maila'
    message = render_to_string('matchmaking/activate_account.html',{
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
        messages.success(request, f'{user}, aby zakończyć rejestracje proszę sprawdź email {to_email} i kliknij w link aktywacyjny.')
    else:
        messages.error(request, f'Problem z wysłaniem maila do {to_email}, sprawdź czy wprowadziłeś poprawny adres email.')

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    with open(os.path.join(settings.BASE_DIR,'register_token.txt')) as f:
        register_key = f.read().strip()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user_reg_key = form.cleaned_data['registration_password']
            if register_key == str(user_reg_key):
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                activateEmail(request, user, form.cleaned_data.get('email'))
                return redirect('login')   
            else:
                messages.info(request, "Błędny kod dostępu")
                return redirect('register') 

    context = {'form': form}
    return render(request, 'matchmaking/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Login lub hasło jest nieprawidłowe')

    context = {}
    return render(request, 'matchmaking/login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    user = None
    if User.objects.filter(username=request.user).exists() and request.user.groups.filter(name="player").exists():
        user = request.user.player
        
    context = {'user': user,}
    return render(request, 'matchmaking/dashboard.html', context)

def matches(request):
    all_matches = Match.objects.all().order_by('match_date')
    today_date = date.today()

    players = {}
    reserve = []
    for match in all_matches:
        players_per_match = match.players.all()
        reserves_per_match = None
        if Reserves.objects.filter(match_id=match).exists():
                reserves = Reserves.objects.get(match_id=match)
                reserves_per_match = reserves.players.all()
        players[match] = {
            'players_per_match': players_per_match,
            'reserves_per_match': reserves_per_match,
            'free_slots': players_per_match.count() + match.reserved_slots
        }                   

    next_matches = searching_for_next_matches(all_matches)
    next_matches_exists = len(next_matches) > 0
    
    context = {'all_matches': all_matches, 'next_matches_exists': next_matches_exists, 'next_matches': next_matches , 'players': players, 'reserve': reserve, 'today_date': today_date}  
    return render(request, 'matchmaking/matches.html', context)

@login_required(login_url='login')
def my_matches(request):
    if User.objects.filter(username=request.user).exists() and request.user.groups.filter(name="player").exists():
        user = request.user.player
        user_matches = []
        matches = Match.objects.all().order_by('-match_date', '-match_time')
        for match in matches:
            match_players = match.players.all()
            if user in match_players:
                user_matches.append(match)
            
            elif user == match.promoter.user.player:
                user_matches.append(match)
                
            elif Reserves.objects.filter(match_id=match).exists():
                reserves = Reserves.objects.get(match_id=match)
                reserves_players = reserves.players.all()
                reserves_players_id = [player_id.player_id for player_id in reserves_players]
                if user in reserves_players_id:
                    user_matches.append(match)       
    else:
        return redirect('login')

    user_matches_exists = len(user_matches) > 0  

    context = {'user_matches': user_matches, 'user_matches_exists': user_matches_exists}
    return render(request, 'matchmaking/my_matches.html', context)

def match(request, pk):
    if request.user.is_authenticated:
        user = request.user.player
        match = Match.objects.get(id=pk)
        players = match.players.all()
        match_datetime = datetime.combine(match.match_date, match.match_time)
        match_datetime_check = match_datetime < datetime.today()
        slots = match.slots
        free_slots = players.count() + match.reserved_slots
        reserve = None
        
        if Reserves.objects.filter(match_id=match).exists():
                    reserve = []
                    reserves = Reserves.objects.get(match_id=match)
                    reserves_players = reserves.players.all()
                    for player in reserves_players:
                        reserve.append(player)
                        
        if reserve is not None:
            reserve_len = len(reserve)
        else:
            reserve_len = 0

        match_mvp = None
        player_rate_result = False
        if MatchPlayersRating.objects.filter(match_id=match).exists():
            match_players_ratings = MatchPlayersRating.objects.get(match_id=match)
            rated_players = match_players_ratings.rated_players.all()
            for player in rated_players:
                if match_mvp is None:
                    match_mvp = player
                else:
                    if player.rate > match_mvp.rate:
                        match_mvp = player
            if PlayerMatchRateDone.objects.filter(player_id=user, match_players_rating_id=match_players_ratings).exists():
                player_rate_status = PlayerMatchRateDone.objects.get(player_id=user, match_players_rating_id=match_players_ratings)
                player_rate_result = player_rate_status

        context = {'player_rate_result': player_rate_result, 'match_mvp': match_mvp, 'user': user, 'match_datetime_check': match_datetime_check, 'free_slots': free_slots, 'match': match, 'players': players, 'slots': slots, 'reserve': reserve, 'reserve_len': reserve_len,}
        if match.promoter.user.id == request.user.id:
            return render(request, 'matchmaking/match_fa.html', context)
        else:
            return render(request, 'matchmaking/match.html', context)
    
    else:
        match = Match.objects.get(id=pk)
        players = match.players.all()
        match_datetime = datetime.combine(match.match_date, match.match_time)
        match_datetime_check = match_datetime < datetime.today()
        slots = match.slots
        free_slots = players.count() + match.reserved_slots
        reserve = None
        
        if Reserves.objects.filter(match_id=match).exists():
                    reserve = []
                    reserves = Reserves.objects.get(match_id=match)
                    reserves_players = reserves.players.all()
                    for player in reserves_players:
                        reserve.append(player)
                        
        if reserve is not None:
            reserve_len = len(reserve)
        else:
            reserve_len = 0

        match_mvp = None
        player_rate_result = False
        if MatchPlayersRating.objects.filter(match_id=match).exists():
            match_players_ratings = MatchPlayersRating.objects.get(match_id=match)
            rated_players = match_players_ratings.rated_players.all()
            for player in rated_players:
                if match_mvp is None:
                    match_mvp = player
                else:
                    if player.rate > match_mvp.rate:
                        match_mvp = player

        context = {'match_mvp': match_mvp, 'match_datetime_check': match_datetime_check, 'free_slots': free_slots, 'match': match, 'players': players, 'slots': slots, 'reserve': reserve, 'reserve_len': reserve_len,}
        return render(request, 'matchmaking/match_guest.html', context)

@login_required(login_url='login')
@check_promoter
def match_fa(request, pk): #full access by promoter
    match = Match.objects.get(id=pk)
    players = match.players.all()
    slots = match.slots
    reserve = []
    reserve_len = len(reserve)

    context = {'match': match, 'players': players, 'slots': slots, 'reserve': reserve, 'reserve_len': reserve_len}
    return render(request, 'matchmaking/match.html', context)

def history(request):
    matches = Match.objects.all().order_by('-match_date')
    matches_history = match_history(matches)

    matches_with_mvp = {}
    for match in matches_history:
        match_mvp = None
        if MatchPlayersRating.objects.filter(match_id=match).exists():
            match_players_ratings = MatchPlayersRating.objects.get(match_id=match)
            rated_players = match_players_ratings.rated_players.all()
            for player in rated_players:
                if match_mvp is None:
                    match_mvp = player
                else:
                    if player.rate > match_mvp.rate:
                        match_mvp = player

        matches_with_mvp[match] = {
            'match': match,
            'mvp': match_mvp,
        }  

    match_history_exists = len(matches_with_mvp) > 0

    context = {'matches_with_mvp': matches_with_mvp, 'match_history_exists': match_history_exists}
    return render(request, 'matchmaking/match_history.html', context)

@login_required(login_url='login')
@check_promoter
def create_match(request):
    player = Player.objects.get(id=request.user.player.id)
    promoters = Promoter.objects.all()
    form = MatchForm()
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            old_match_date = form.cleaned_data['match_date']
            new_format_match_date = old_match_date.strftime('%Y/%d/%m')
            form.cleaned_data['match_date'] = new_format_match_date
            match = form.save(commit=False)
            for promoter in promoters:
                if promoter.user == player.user:
                    match.promoter = promoter
            match.save()
            if form.is_valid():
                form.save()
                return redirect('match', pk=match.id)
        else:
            context = {}
            return redirect('create_match_form_error')

    context = {'form': form}
    return render(request, 'matchmaking/create_match_form.html', context)

@login_required(login_url='login')
@check_promoter
def create_match_again(request, pk):
    match = Match.objects.get(id=pk)
    form = MatchAgainForm(instance=match)
    
    if request.method == 'POST':
        form = MatchAgainForm(request.POST, instance= match)
        if form.is_valid():
            new_match = Match.objects.create(
                name = form.cleaned_data['name'],
                skill_level = form.cleaned_data['skill_level'],
                reserved_slots = form.cleaned_data['reserved_slots'],
                slots = form.cleaned_data['slots'],
                match_cost = form.cleaned_data['match_cost'],
                localization = form.cleaned_data['localization'],
                match_date = form.cleaned_data['match_date'],
                match_time = form.cleaned_data['match_time'],
                promoter = match.promoter
            )
            if form.cleaned_data['same_players'] == True:
                new_match.players.set(match.players.all())
            new_match.save()
            return redirect('match', pk=new_match.id)

    context = {'form': form, 'match': match}
    return render(request, 'matchmaking/create_match_again.html', context)

@login_required(login_url='login')
@check_promoter
def create_match_form_error(request):

    context = {}
    return render(request, 'matchmaking/create_match_form_error.html', context)

@login_required(login_url='login')
def create_match_error(request):

    context = {}
    return render(request, 'matchmaking/create_match_error.html', context)

@login_required(login_url='login')
def red_card_error(request):

    context = {}
    return render(request, 'matchmaking/red_card_error.html', context)

@login_required(login_url='login')
@check_promoter
def add_permission_error(request):

    context = {}
    return render(request, 'matchmaking/add_permission_error.html', context)

@login_required(login_url='login')
@check_promoter
def add_permissions(request):
    form = AddPermissionsForm()
    
    if request.method == 'POST':
        form = AddPermissionsForm(request.POST)
        if form.is_valid():
            new_promoter_name = form.cleaned_data['name']
            if Player.objects.filter(name=new_promoter_name).exists():
                new_promoter_player= Player.objects.get(name = new_promoter_name)

                new_promoter = Promoter.objects.create(
                    user = new_promoter_player.user,
                    name = new_promoter_player.name,
                    player = new_promoter_player,
                )
                new_promoter.save()
                return redirect('home')
            else:
                return redirect('add_permission_error')

    context = {'form': form, 'match': match}
    return render(request, 'matchmaking/add_permissions.html', context)

@login_required(login_url='login')
@check_promoter
def registration_token_change(request):
    form = RegistrationTokenChangeForm()
    
    if request.method == 'POST':
        form = RegistrationTokenChangeForm(request.POST)
        if form.is_valid():
            new_token = form.cleaned_data['new_token']
            with open(os.path.join(settings.BASE_DIR,'register_token.txt'), 'w') as f:
                f.write(new_token)
            return redirect('home')

    context = {'form': form, 'match': match}
    return render(request, 'matchmaking/registration_token_change.html', context)

@login_required(login_url='login')
def add_comment(request, pk):
    match = Match.objects.get(id=pk)
    form = CommentForm(instance=match)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance= match)
        if form.is_valid():
            new_comment = Comments.objects.create(
                match_id = match,
                user = request.user,
                body = form.cleaned_data['body']
            )
            new_comment.save()
            form.save()
            match.save()
            return redirect('match', pk=match.id)

    context = {'form': form, 'match': match}
    return render(request, 'matchmaking/add_comment.html', context)

@login_required(login_url='login')
@check_promoter
def update_match(request, pk):
    match = Match.objects.get(id=pk)
    form = MatchForm(instance=match)
    
    if request.method == 'POST':
        form = MatchForm(request.POST, instance= match)
        if form.is_valid():
            form.save()
            return redirect('match', pk=match.id)

    context = {'form': form, 'match': match}
    return render(request, 'matchmaking/update_match.html', context)

@login_required(login_url='login')
@check_promoter
def update_match_players(request, pk):
    match = Match.objects.get(id=pk)
    players_to_kick = None
    form = MatchPlayersForm(instance=match, current_match=match)

    if request.method == 'POST':
        form = MatchPlayersForm(request.POST, instance= match, current_match=match)
        if form.is_valid():
            players_to_kick = form.cleaned_data['players']
    
    if players_to_kick is not None:
        for player in players_to_kick:
            match.players.remove(player)
            match.save()
        return redirect('match', pk= match.id)

    context = {'form': form, 'match': match}
    return render(request, 'matchmaking/update_match_players.html', context)

@login_required(login_url='login')
@check_promoter
def update_match_result(request, pk):
    match = Match.objects.get(id=pk)
    form = MatchResultForm(instance=match)
    
    if request.method == 'POST':
        form = MatchResultForm(request.POST, instance= match)
        if form.is_valid():
            form.save()
            return redirect('match', pk=match.id)

    context = {'form': form, 'match': match}
    return render(request, 'matchmaking/update_match_result.html', context)

@login_required(login_url='login')
@check_promoter
def kick_player(request, match_pk, player_pk):
    match = Match.objects.get(id=match_pk)
    player = Player.objects.get(id=player_pk)
    form = MatchForm()

    if request.method == 'POST':
        match.players.remove(player)
        match.save()
        return redirect('match', pk=match.id)

    context = {'form': form, 'match': match, 'player': player}
    return render(request, 'matchmaking/kick_player_form.html', context)

@login_required(login_url='login')
@check_promoter
def yellow_card_assign(request, match_pk, player_pk):
    match = Match.objects.get(id=match_pk)
    player = Player.objects.get(id=player_pk)
    form = PlayerForm()

    if request.method == 'POST':
        if player.yellow_cards >= 1:
            player.yellow_cards = 0
            player.red_cards += 1
        else:
            player.yellow_cards += 1
        player.save()
        return redirect('match', pk=match.id)

    context = {'form': form, 'match': match, 'player': player}
    return render(request, 'matchmaking/yellow_card_assign_form.html', context)

@login_required(login_url='login')
@check_promoter
def red_card_assign(request, match_pk, player_pk):
    match = Match.objects.get(id=match_pk)
    player = Player.objects.get(id=player_pk)
    form = PlayerForm()

    if request.method == 'POST':
        player.red_cards += 1
        player.save()
        return redirect('match', pk=match.id)

    context = {'form': form, 'match': match, 'player': player}
    return render(request, 'matchmaking/red_card_assign_form.html', context)

@login_required(login_url='login')
@check_promoter
def reserve_slots(request, pk):
    match = Match.objects.get(id=pk)
    form = ReserveSlotsForm(instance=match)

    if request.method == 'POST':
        form = ReserveSlotsForm(request.POST, instance= match)
        if form.is_valid():

            form.save()
            return redirect('match', pk=match.id)

    context = {'match': match, 'form': form}
    return render(request, 'matchmaking/reserve_slots.html', context)


@login_required(login_url='login')
@check_promoter
def delete_match(request, pk):
    match = Match.objects.get(id=pk)
    form = MatchForm()

    if request.method == 'POST':
        match.delete()
        return redirect('matches')

    context = {'form': form, 'match': match}
    return render(request, 'matchmaking/delete_match_form.html', context)

@login_required(login_url='login')
def join_match(request, pk):
    player = request.user.player
    match = Match.objects.get(id=pk)
                
    if request.method == 'POST':
        if player.red_cards >= 1:
            context = {}
            return redirect('red_card_error')

        if player in match.players.all():
            return redirect('/')

        if match.players.count() + match.reserved_slots < match.slots:
            if ReservesPlayer.objects.filter(match_id=match, player_id=player).exists():
                reserve_player = ReservesPlayer.objects.get(match_id=match, player_id=player)
                reserve_player.delete()
                match.players.add(player)
            else:    
                match.players.add(player)
        else:
            if Reserves.objects.filter(match_id=match).exists():
                reserve = Reserves.objects.get(match_id=match)
                if ReservesPlayer.objects.filter(match_id=match, player_id=player).exists():
                    pass
                else:
                    new_player = ReservesPlayer.objects.create(
                        match_id = match,
                        player_id=player,
                    )
                    reserve.players.add(new_player)
            else:        
                match.reserves = Reserves(
                    match_id = match,
                )
                match.reserves.save()
                new_player = ReservesPlayer.objects.create(
                    match_id = match,
                    player_id=player,
                )
                match.reserves.players.add(new_player)
        match.save()
        return redirect('match', pk=match.id)

    context = {'match': match, 'player': player}
    return render(request, 'matchmaking/join_match_form.html', context)

@login_required(login_url='login')
def leave_match(request, pk):
    player = request.user.player
    match = Match.objects.get(id=pk)
    match_players = match.players.all()
    form = MatchForm()
    reserves_players = None

    if request.method == 'POST':
        if Reserves.objects.filter(match_id=match).exists():
                reserves = Reserves.objects.get(match_id=match)
                reserves_players = reserves.players.all()

        if reserves_players is None:
            if player in match_players:
                match.players.remove(player)
                match.save()

        if reserves_players is not None:
            if player in match_players:
                match.players.remove(player)
                if len(reserves_players) != 0 and match.reserved_slots + match.players.count() < match.slots:
                    new_player = reserves_players[0]
                    match.players.add(new_player.player_id)
                    reserves.players.remove(new_player)
                    reserved_player = ReservesPlayer.objects.get(match_id=match, player_id=new_player.player_id)
                    reserved_player.delete()
                match.save()
                reserves.save()
            else:
                for reserve_player in reserves_players:
                    if player == reserve_player.player_id:
                        reserves.players.remove(reserve_player)
                        reserved_player = ReservesPlayer.objects.get(match_id=match, player_id=player)
                        reserved_player.delete()
                        reserves.save()

        return redirect('match', pk=match.id)

    context = {'form': form, 'match': match, 'player': player}
    return render(request, 'matchmaking/leave_match_form.html', context)

@login_required(login_url='login')
def profile(request):
    player = request.user.player
    groups = None

    matches = request.user.player.match_set.all().order_by('-match_date')
    if matches is not None:
        last_5_matches = []
        for index, match in enumerate(matches):
            if index < 5:
                last_5_matches.append(match)
    
    else:
        last_5_matches = None

    def has_related_object(user_check):
        return hasattr(user_check, 'promoter')

    if has_related_object(request.user):
        organize_matches = request.user.promoter.match_set.all().order_by('-match_date')
        last_5_organized_matches = []
        for index, match in enumerate(organize_matches):
            if index < 5:
                last_5_organized_matches.append(match)

    else:
        last_5_organized_matches = None

    context = {'groups': groups, 'player': player, 'matches': last_5_matches, 'organized_matches': last_5_organized_matches}
    return render(request, 'matchmaking/profile.html', context)

def playerPage(request, pk):
    player = Player.objects.get(id=pk)

    all_matches = Match.objects.all().order_by('match_date')

    matches_with_mvp = {}
    for match in all_matches:
        rate = 0
        if MatchPlayersRating.objects.filter(match_id=match).exists():
            match_players_ratings = MatchPlayersRating.objects.get(match_id=match)
            match_rated_players = match_players_ratings.rated_players.all()
            for rated_player in match_rated_players:
                if player == rated_player.player_id:
                    rate = int(rated_player.rate)

        matches_with_mvp[match] = {
            'match': match,
            'rate': rate,
        }  

    context = {'player': player, 'matches_with_mvp': matches_with_mvp}
    return render(request, 'matchmaking/player.html', context)

@login_required(login_url='login')
def rate_players(request, pk):
    match = Match.objects.get(id=pk)
    rated_players=None
    form = PlayerRatingForm( current_match=match)

    if request.method == 'POST':
        form = PlayerRatingForm(request.POST, current_match=match)
        if form.is_valid():
            rated_players = form.cleaned_data['players']
    
    if rated_players is not None:   
        if MatchPlayersRating.objects.filter(match_id=match).exists():
            match_ratings = MatchPlayersRating.objects.get(match_id=match)
            already_rated_players = match_ratings.rated_players.all()
            already_rated_players_id = [player.player_id for player in already_rated_players]
            for player in rated_players:
                if player in already_rated_players_id:
                    player_data = PlayerRating.objects.get(match_id=match, player_id=player)
                    player_data.rate += 1
                    player_data.save()
                else:
                    player_new_object = PlayerRating.objects.create(
                        match_id = match,
                        player_id=player,
                        rate= 1
                    )
                    match_ratings.rated_players.add(player_new_object)
                    match_ratings.save()
                    
        else:
            match_ratings = MatchPlayersRating.objects.create(
                        match_id= match,
                    )
            for player in rated_players:
                new_player_rate = PlayerRating.objects.create(
                                match_id = match,
                                player_id = player,
                                rate = 1
                                )
                match_ratings.rated_players.add(new_player_rate)
                match_ratings.save()

        PlayerMatchRateDone.objects.create(
            player_id = request.user.player,
            match_players_rating_id = match_ratings,
            rate_done = True
        )
        return redirect('match', pk=match.id)  

    context = {'form': form, 'match': match}
    return render(request, 'matchmaking/rate_players.html', context)

@login_required(login_url='login')
def update_player(request, pk):
    player = Player.objects.get(id=pk)
    form = PlayerForm(instance=player)
    
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance= player)
        if form.is_valid():
            form.save()
            return redirect('profile')  

    context = {'form': form, 'player': player}
    return render(request, 'matchmaking/update_player.html', context)

@login_required(login_url='login')
def promoter(request, pk):
    promoter = Promoter.objects.get(id=pk)
    matches = promoter.match_set.all()

    context = {'promoter': promoter, 'matches': matches}
    return render(request, 'matchmaking/promoter.html', context)

@login_required(login_url='login')
def create_ticket(request, pk):
    player = Player.objects.get(id=pk)
    form = AddTicketForm()
    if player.ticket_counter >= 5:
        return redirect('ticket_count_error')

    if request.method == 'POST':
        form = AddTicketForm(request.POST)
        if form.is_valid():
            new_ticket = Ticket.objects.create(
                player_id = player,
                title = form.cleaned_data['title'],
                body = form.cleaned_data['body'],
            )
            new_ticket.save()
            player.ticket_counter += 1
            player.save()
            return redirect('home')  

    context = {'form': form, 'player': player}
    return render(request, 'matchmaking/create_ticket.html', context)

@login_required(login_url='login')
@check_promoter
def tickets(request):
    all_tickets = Ticket.objects.all()
    tickets_exists = len(all_tickets) > 0

    context = {'all_tickets': all_tickets, 'tickets_exists': tickets_exists}
    return render(request, 'matchmaking/tickets.html', context)

@login_required(login_url='login')
@check_promoter
def ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)

    context = {'ticket': ticket}
    return render(request, 'matchmaking/ticket.html', context)

@login_required(login_url='login')
@check_promoter
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if ticket.title == "Czerwona kartka":
        player = Player.objects.get(id=ticket.player_id.id)
        player.red_cards = 0
        player.ticket_counter -= 1
        player.save()

    if ticket.title == "Dostęp do organizowania meczy":
        player = Player.objects.get(id=ticket.player_id.id)
        if not Promoter.objects.filter(user=player.user).exists():
            new_promoter = Promoter.objects.create(
                user = player.user,
                name = player.name,
                phone = player.phone,
                email = player.email,
                player = player,
            )
            new_promoter.save()
            player.ticket_counter -= 1
            player.save()
    ticket.delete()

    context = {}
    return render(request, 'matchmaking/tickets.html', context)

@login_required(login_url='login')
@check_promoter
def decline_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    player = Player.objects.get(id=ticket.player_id.id)
    ticket.delete()
    player.ticket_counter -= 1
    player.save()

    context = {}
    return render(request, 'matchmaking/tickets.html', context)

@login_required(login_url='login')
def ticket_count_error(request):

    context = {}
    return render(request, 'matchmaking/ticket_count_error.html', context)