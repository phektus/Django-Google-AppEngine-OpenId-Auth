from django import forms

class OpenIDLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        label='Google email',
        widget=forms.TextInput(attrs={'class': 'required email'}))
