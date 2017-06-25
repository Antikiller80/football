from django.db import models
from django.db.models import Q
from django.db.models import Sum
from ckeditor_uploader.fields import RichTextUploadingField
# сделать property с таблицы матч евент общие количестов к,ж карточек

position_choices = (
        ('goalkeeper', 'Вратарь'),
        ('defender', 'Защитник'),
        ('halfback', 'Полузащитник'),
        ('forward', 'Нападающий'),
    )


class Championship(models.Model):
    name_championship = models.CharField('Название чемпионата', max_length=50, blank=True, null=True)
    description = RichTextUploadingField('Описание', blank=True, default='')

    class Meta:
        verbose_name = 'чемпионат'
        verbose_name_plural = 'чемпионаты'

    def __str__(self):
        return "{0}".format(self.name_championship)


class Player(models.Model):
    name = models.CharField('Имя игрока', max_length=50, blank=True)
    position = models.CharField('Позиция', max_length=10, choices=position_choices)
    number = models.IntegerField('Номер игрока', blank=True)
    citizenship = models.CharField('Гражданство', max_length=20, blank=True, null=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    foto = models.ImageField('Фото игрока', blank=True, null=True, upload_to='players_images/')

    class Meta:
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'

    def get_photo(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return '/static/default_images/default_photo.png'

    def get_last_club(self):
        return self.clubs.all().last()

    def __str__(self):
        return "{0}".format(self.name)

    @property
    def red_card(self):
        return MatchEvent.objects.filter(Q(event_match="red_card") & Q(player=self)).count()

    @property
    def yellow_card(self):
        return MatchEvent.objects.filter(Q(event_match="yellow_card") & Q(player=self)).count()

    @property
    def goals(self):
        return MatchEvent.objects.filter(Q(event_match="goal") & Q(player=self)).exclude(event_match="autogoal").count()

    @property
    def penalty(self):
        return MatchEvent.objects.filter(Q(event_match="penalty") & Q(player=self)).count()

    @property
    def assists(self):
        return MatchEvent.objects.filter(Q(event_match="assists") & Q(player=self)).count()

    @property
    def matches_played(self):
        a = Matches.objects.filter(guest_players=self).count()
        b = Matches.objects.filter(home_players=self).count()
        return a+b


class Club(models.Model):
    championships = models.ManyToManyField(Championship, related_name='clubs', verbose_name='Чемпионат')
    players = models.ManyToManyField(Player, related_name='clubs', verbose_name='Игроки')
    name = models.CharField('Название клуба', max_length=30, blank=True)
    main_coach = models.CharField('Главный тренер', max_length=50, null=True, blank=True)
    logo = models.ImageField('Логотип клуба', blank=True, null=True, upload_to='club_images/')
    based = models.DateField('Дата основания', null=True, blank=True)
    color = models.CharField('Цвет', max_length=50, blank=True, null=True)
    achievement = RichTextUploadingField('Достижения', blank=True, null=True)
    stadium = models.CharField('Стадион', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'клуб'
        verbose_name_plural = 'клубы'

    def get_photo(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return '/static/default_images/default_photo.png'

    def __str__(self):
        return "{0}".format(self.name)

    @property
    def matches_sum(self):
        return Matches.objects.filter(Q(home_club=self) | Q(guest_club=self)).count()

    @property
    def winned_matches(self):
        matches = Matches.objects.filter(Q(home_club=self) | Q(guest_club=self))
        return sum([1 if match.win_club == self else 0 for match in matches])

    @property
    def losed_matches(self):
        matches = Matches.objects.filter(Q(home_club=self) | Q(guest_club=self))
        return sum([1 if match.win_club != self and match.win_club != "draw" else 0 for match in matches])

    @property
    def drawed_matches(self):
        matches = Matches.objects.filter(Q(home_club=self) | Q(guest_club=self))
        return sum([1 if match.win_club == "draw" else 0 for match in matches])

    @property
    def points(self):
        earned_points = self.winned_matches * 3 + self.drawed_matches
        penalties = PenaltyClub.objects.filter(club=self)
        for penalty in penalties:
            earned_points += penalty.point
        return earned_points

    @property
    def goals_scored(self):
        goals_home = Matches.objects.filter(home_club=self).aggregate(Sum('goals_home'))
        goals_guest = Matches.objects.filter(guest_club=self).aggregate(Sum('goals_guest'))
        return sum(goals_guest.values()) + sum(goals_home.values())

    @property
    def goals_missed(self):
        goals_home = Matches.objects.filter(home_club=self).aggregate(Sum('goals_guest'))
        goals_guest = Matches.objects.filter(guest_club=self).aggregate(Sum('goals_home'))
        return sum(goals_guest.values()) + sum(goals_home.values())

    @property
    def goal_difference(self):
        return self.goals_scored - self.goals_missed


class Matches(models.Model):
    home_club = models.ForeignKey(Club, related_name='home_club', blank=True, verbose_name='Домашний клуб')
    guest_club = models.ForeignKey(Club, related_name='guest_club', blank=True, verbose_name='Гостевой клуб')
    сhampionship = models.ForeignKey(Championship, related_name='league', verbose_name='Чемпионат')
    home_players = models.ManyToManyField(Player, related_name='home_players', blank=True, verbose_name='Состав домашней команды')
    guest_players = models.ManyToManyField(Player, related_name='guest_players', blank=True, verbose_name='Состав гостевой команды')
    tour = models.IntegerField('Тур', blank=True)
    match_date = models.DateTimeField('День матча', null=True, blank=True)
    goals_home = models.IntegerField('Забито дома', blank=True, null=True)
    goals_guest = models.IntegerField('Забито гостями', blank=True, null=True)

    class Meta:
        verbose_name = 'матч'
        verbose_name_plural = 'матчи'
        ordering = ['tour', 'match_date']

    def __str__(self):
        return "{} - {}".format(self.home_club, self.guest_club)

    @property
    def win_club(self):
        if self.goals_guest is None and self.goals_home is None:
            return "Матч не сыгран"
        elif self.goals_guest < self.goals_home:
            return self.home_club
        elif self.goals_guest > self.goals_home:
            return self.guest_club
        else:
            return "draw"


class MatchEvent(models.Model):
    event_choices = (
        ('replacement', 'Замена'),
        ('yellow_card', 'Жёлтая карточка'),
        ('red_card', 'Красная карточка'),
        ('goal', 'Гол'),
        ('autogoal', 'автогол'),
    )
    #choice event(пенальти, ассист, карточка и т.д 5 событий)
    player = models.ForeignKey(Player, verbose_name='Игрок')
    match = models.ForeignKey(Matches, verbose_name='матч', related_name='events')
    event_time = models.CharField('Время события', max_length=50)
    event_match = models.CharField('Собитие', max_length=50, choices=event_choices)

    class Meta:
        verbose_name = 'событие матча'
        verbose_name_plural = 'события матча'
        ordering = ['event_time']

    def __str__(self):
        return "{0}".format(self.event_match)


class PenaltyClub(models.Model):
    club = models.ForeignKey(Club, verbose_name='Клуб', related_name='penalties')
    point = models.IntegerField('Очки',)
    reason = RichTextUploadingField('Причина', blank=True, null=True)

    class Meta:
        verbose_name = 'наказание'
        verbose_name_plural = 'наказания'

    def __str__(self):
        return "{0}".format(self.club)


