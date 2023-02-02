from dataclasses import field
from django.forms import ModelForm, TextInput, NumberInput, Select, EmailInput, ModelChoiceField, DateInput, TimeInput, Textarea, BooleanField
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


    
class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ['name','skill_level', 'slots', 'reserved_slots', 'match_cost', 'localization', 'match_date', 'match_time',]
        widgets ={
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Nazwa'
                }),
            'skill_level': Select(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Poziom umiejętności',
                }),
            'slots': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Ilość miejsc',
                }),
            'reserved_slots': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Zarezerwowane miejsca',
                }),
            'match_cost': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Koszt meczu',
                }),
            'localization': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Lokalizacja',
                }),
            'match_date': DateInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'np. 2022-12-20',

                }),
            'match_time': TimeInput(format="%H:%M",attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'np. 12:30',
                }),
        }

class MatchAgainForm(ModelForm):
    class Meta:
        model = Match
        fields = ['name','skill_level', 'slots', 'reserved_slots', 'match_cost', 'localization', 'match_date', 'match_time',]
        widgets ={
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Nazwa'
                }),
            'skill_level': Select(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Poziom umiejętności',
                }),
            'slots': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Ilość miejsc',
                }),
            'reserved_slots': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Zarezerwowane miejsca',
                }),
            'match_cost': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Koszt meczu',
                }),
            'localization': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Lokalizacja',
                }),
            'match_date': DateInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'np. 2022-12-20',

                }),
            'match_time': TimeInput(format="%H:%M",attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'np. 12:30',
                }),
        }
    
    def __init__(self, *args, **kwargs):
        super(MatchAgainForm, self).__init__(*args, **kwargs)
        self.fields['same_players'] = BooleanField(label="Kopiuj zawodników")
        self.fields['same_players'].required = False

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['body']
        widgets ={
            'body': Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Dodaj komentarz'
                }),
        }

class AddTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'body']
        widgets ={
            'title': Select(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                }),
            'body': Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Dodaj komentarz'
                }),
            
        }

class MatchPlayersForm(ModelForm):
    class Meta:
        model = Match
        fields = ['players']
        
    def __init__(self, *args, **kwargs):
        current_match = kwargs.pop('current_match', None) 
        super(MatchPlayersForm, self).__init__(*args, **kwargs)
        match_players = current_match.players.all()
        self.fields['players'].label = "Uczestnicy: "
        self.fields['players'].queryset = match_players
        self.fields['players'].widgets = ModelChoiceField(queryset=match_players)


class MatchResultForm(ModelForm):
    class Meta:
        model = Match
        fields = ['match_result']
        widgets ={
            'match_result': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100px;',
                }),
        }

class ReserveSlotsForm(ModelForm):
    class Meta:
        model = Match
        fields = ['reserved_slots']
        widgets ={
            'reserved_slots': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 80px;',
                }),
        }

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'nickname', 'favorite_position', 'phone', 'email']
        widgets ={
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Nazwa'
                }),
            'nickname': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Ksywka'
                }),
            'favorite_position': Select(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                }),
            'phone': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Numer telefonu',
                }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email',
                }),
        }

class PlayerRatingForm(ModelForm):
    class Meta:
        model = Match
        fields = ['players']
        
    def __init__(self, *args, **kwargs):
        current_match = kwargs.pop('current_match', None) 
        super(PlayerRatingForm, self).__init__(*args, **kwargs)
        match_players = current_match.players.all()
        self.fields['players'].label = "Uczestnicy: "
        self.fields['players'].queryset = match_players
        self.fields['players'].widgets = ModelChoiceField(queryset=match_players)

class CreateUserForm(UserCreationForm):
    registration_password = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'registration_password']

class AddPermissionsForm(ModelForm):
    name = forms.CharField(max_length=100)
    class Meta:
        model = Player
        fields = ['name']
        
    def __init__(self, *args, **kwargs):
        super(AddPermissionsForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nazwa: "
        self.fields['name'].widget.attrs['style'] = 'width:200px;'

class RegistrationTokenChangeForm(ModelForm):
    new_token = forms.CharField(max_length=100)
    class Meta:
        model = Player
        fields = ['new_token']
        
    def __init__(self, *args, **kwargs):
        super(RegistrationTokenChangeForm, self).__init__(*args, **kwargs)
        self.fields['new_token'].label = "Kod dostępu: "
        self.fields['new_token'].widget.attrs['style'] = 'width:200px;'