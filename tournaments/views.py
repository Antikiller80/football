import operator
from django.shortcuts import render
from django.views.generic import DetailView
from tournaments.models import Player, Club, Championship, Matches
from itertools import zip_longest
from django.db.models import Q


class PlayerDetailView(DetailView):
    model = Player
    context_object_name = 'player'
    template_name = 'tournaments/detail_player.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        return context


class ClubDetailView(DetailView):
    model = Club
    context_object_name = 'club'
    template_name = 'tournaments/detail_club.html'

    def get_context_data(self, **kwargs):
        context = super(ClubDetailView, self).get_context_data(**kwargs)
        #доделать вывод по конкретному клубу (пока выводит все матчи)
        context['matches'] = Matches.objects.filter(Q(home_club__name__icontains=self.object) | Q(guest_club__name__icontains=self.object)).order_by('match_date')
        return context


class ChampionshipDetailView(DetailView):
    model = Championship
    context_object_name = 'championship'
    template_name = 'tournaments/detail_championship.html'
    queryset = Championship.objects.all().prefetch_related('clubs')

    def get_context_data(self, **kwargs):
        context = super(ChampionshipDetailView, self).get_context_data(**kwargs)
        context['clubs'] = sorted(Championship.objects.all()[0].clubs.all(), key=lambda x: (x.points, x.goal_difference), reverse=True)
        context['tour_detail'] = Matches.objects.all()

        return context


class MatchesDetailView(DetailView):
    model = Matches
    context_object_name = 'matches'
    template_name = 'tournaments/detail_matches.html'

    def get_context_data(self, **kwargs):
        context = super(MatchesDetailView, self).get_context_data(**kwargs)
        #объднение двух списков игроков и команд с помощью zip_longets (соединяет 1 эл с 1эл списков, при пустоте fillvalue)
        context['teams'] = zip_longest(context['matches'].home_players.all(), context['matches'].guest_players.all(), fillvalue='')
        return context


def matchtourdetail(request, tour=None):
    tour_number = Matches.objects.filter(tour=tour)
    context = {'tour_number': tour_number}
    return render(request, 'tournaments/detail_tour.html', context)
