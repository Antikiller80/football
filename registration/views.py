import hashlib, datetime, random

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from registration.forms import RegistrationForm, ProfileEditForm
from registration.models import Profile
from tournaments.models import Player, Club


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/registration/login/")


class RegisterFormView(FormView):
    form_class = RegistrationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/registration/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        user = form.save()
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
        activation_key = hashlib.sha1(str(salt + email).encode('utf-8')).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        # Get user by username
        # Create and save user profile
        profile = Profile.objects.get(user=user)
        if profile:
            profile.activation_key = activation_key
            profile.key_expires = key_expires
            profile.save()
        else:
            profile = Profile.objects.create(user=user, activation_key=activation_key, key_expires=key_expires)
            profile.save()

        # Send email with activation key
        email_subject = 'registration'
        email_body = "Hey {}, thanks for signing up. To activate your account, click this link within \
        48hours http://127.0.0.1:8000/registration/confirm/{}".format(username, activation_key)
        from django.conf import settings
        send_mail(email_subject, email_body, settings.ADMIN_EMAIL, [email, ], fail_silently=False)

        return super(RegisterFormView, self).form_valid(form)


def register_confirm(request, activation_key):
    user_profile = get_object_or_404(Profile, activation_key=activation_key)
    if request.user.is_authenticated():
        HttpResponseRedirect('/')
    if user_profile.key_expires < timezone.now():
        return render(request, 'registration/confirm_expired.html')
    user = user_profile.user
    user.is_active = True
    user.save()
    return render(request, 'registration/confirm.html')


class LoginFormView(FormView):
    form_class = AuthenticationForm
    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "registration/login.html"
    # В случае успеха перенаправим на главную.
    success_url = "/registration/login/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class ProfileUpdate(DetailView):
    form_class = ProfileEditForm
    initial = {'pk': 'pk'}
    template_name = 'registration/update.html'
    model = Profile

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            # user = form.save(commit=False)
            birth_date = form.cleaned_data.pop('birth_date')
            favourite_team = form.cleaned_data.pop('favorite_team')
            location = form.cleaned_data.pop('location')
            favorite_player = form.cleaned_data.pop('favorite_player')
            profile = Profile.objects.filter(user=user)[0]
            profile.birth_date = birth_date
            profile.favorite_team = favourite_team
            profile.location = location
            profile.favorite_player = favorite_player
            profile.save()
            favourite_players = favorite_player.split(',')
            for player_name in favourite_players:
                finded_players = Player.objects.filter(name__icontains=player_name.strip())
                if finded_players.exists():
                    player_inst = Player.objects.filter(name__icontains=player_name.strip())[0]
                    profile.favorite_players.add(player_inst)
            profile.save()
            favourite_teams = favourite_team.split(',')
            for club_name in favourite_teams:
                finded_clubs = Club.objects.filter(name__icontains=club_name.strip())
                if finded_clubs.exists():
                    club_inst = Club.objects.filter(name__icontains=club_name.strip())[0]
                    profile.favorite_teams.add(club_inst)
            profile.save()
            form.save()
            messages.add_message(request, messages.INFO, "Данные пользователя успешно сохранены!")
        else:
            form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user != profile.user:
            return render(request, 'registration/no_login_user.html')
        else:
             return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)
    # def dispatch(self, request, pk, *args, **kwargs):
    #     user = get_object_or_404(User, pk=pk)
    #     profile = Profile.objects.filter(user=user)[0]
    #     if request.user != profile.user:
    #          return render(request, 'registration/no_login_user.html')
    #     else:
    #         return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'registration/detail_user.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user != profile.user:
             return render(request, 'registration/no_login_user.html')
        else:
            return super(ProfileView, self).dispatch(request, *args, **kwargs)
