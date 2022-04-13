from django import forms
from .models import *


class NewsForm(forms.ModelForm):
    image = forms.FileField(required=True)

    def save(self, commit=True):
        instance = super(NewsForm, self).save(commit=False)
        f = self['image'].data.read()
        instance.image = base64.b64encode(f)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = News
        fields = ['title', 'text']
