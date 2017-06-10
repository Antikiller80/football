from django.contrib import admin

from .models import Championship, Player, Club, Matches, MatchEvent, PenaltyClub


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'citizenship',)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MatchAdmin(admin.ModelAdmin):
    fields = ('winner_command', 'home_club', 'guest_club', 'home_players', 'guest_players', 'сhampionship', 'tour', 'match_date', 'goals_home', 'goals_guest')
    readonly_fields = ('winner_command', )
    list_display = ('tour', 'match_date', 'сhampionship',  "score", )

    def winner_command(self, obj):
        return "Ничья" if obj.win_club == "draw" else obj.win_club

    winner_command.short_description = "Команда победитель"

    def score(self, obj):
        return "{} {}:{} {}".format(obj.home_club, obj.goals_home, obj.goals_guest, obj.guest_club)

    score.short_description = "Матч"


class MatchEventAdmin(admin.ModelAdmin):
    list_display = ('event_match', 'match')


class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('club', 'point', 'reason')

admin.site.register(Championship)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Matches, MatchAdmin)
admin.site.register(MatchEvent, MatchEventAdmin)
admin.site.register(PenaltyClub, PenaltyAdmin)
