from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False  # not active until he opens activation link
            user.save()
            return user

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Пользователь с таким email уже существует. Пожалуйста укажите другой email")


class ProfileEditForm(forms.ModelForm):
    location = forms.CharField(max_length=30, required=False, label='Страна')
    birth_date = forms.DateField(required=False, label='День рождения')
    favorite_team = forms.CharField(max_length=50, required=False, label='Любимая команда')
    favorite_player = forms.CharField(max_length=50, required=False, label='Любимый игрок')

    class Meta:
        model = User
        fields = ('email', 'location', 'birth_date', 'favorite_team', 'favorite_player')
