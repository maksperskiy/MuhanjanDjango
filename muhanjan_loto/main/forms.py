from django import forms
from .models import *

class LobbyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['game'].empty_label = 'Choose game'

    class Meta:
        model = Lobby
        fields = ['name', 'max_users', 'password', 'game']

    
    def clean_max_users(self):
        max_users = self.cleaned_data['max_users']
        game_id = self.data['game']
        
        if max_users < 1:
            raise forms.ValidationError('Cannot be zero or negative')
        if max_users > Game.objects.filter(id = game_id).values('max_users').first()['max_users']:
            raise forms.ValidationError('Cannot be more than game max_users')

        return max_users
