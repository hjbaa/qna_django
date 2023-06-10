from django import forms
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loginName'}),
        label='Username'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'loginPassword'}),
        label='Password'
    )

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            profile = Profile.objects.get_profile_by_username(username)
            if not profile or not profile.user.check_password(password):
                self.add_error(None, 'Wrong username or password')

        return self.cleaned_data


class SignupForm(forms.Form):
    ...
