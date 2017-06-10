import datetime

from django.db.models import Q

from post.models import Category, Article
from tournaments.models import Championship, Matches, Player


def table(request):
    clubes = Championship.objects.all()[0]
    table = sorted(clubes.clubs.all(), key=lambda x: (x.points, x.goal_difference), reverse=True)
    match_all = Matches.objects.all()
    date = datetime.date.today()
    match_day = match_all.filter(match_date__date=date)
    players = Player.objects.all()
    table_players = sorted(players, key=lambda x: (x.goals), reverse=True)[0:10]
    return {"table": table,
            "match_day": match_day,
            "table_players": table_players, }


def category(request):
    categors = Category.objects.all()
    return {"categors": categors}


def article(request):
    arti = Article.objects.all()[0:4]
    return {"arti": arti}
