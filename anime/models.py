from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

ANIME_TYPES = [
    (0, u'TV'),
    (1, u'Movie'),
    (2, u'OAV'),
    (3, u'TV-Sp'),
    (4, u'SMovie'),
    (5, u'ONA'),
    (6, u'AMV')
    ]

ANIME_GENRE = [
    (0, u'action'),
    (1, u'adventure'),
    (2, u'children'),
    (3, u'comedy'),
    (4, u'cyberpunk'),
    (5, u'daily life'),
    (6, u'detective'),
    (7, u'drama'),
    (8, u'ecchi'),
    (9, u'fairy tale'),
    (10, u'fantastic'),
    (11, u'fantasy'),
    (12, u'hentai'),
    (13, u'history'),
    (14, u'horror'),
    (15, u'maho shodjo'),
    (16, u'martial arts'),
    (17, u'mecha'),
    (18, u'music'),
    (19, u'mystery'),
    (20, u'parody'),
    (21, u'police'),
    (22, u'postapocalyptic'),
    (23, u'psychology'),
    (24, u'romance'),
    (25, u'samurai'),
    (26, u'school'),
    (27, u'shojo'),
    (28, u'shodjo-ai'),
    (29, u'shonen'),
    (30, u'sport'),
    (31, u'steampunk'),
    (32, u'thriller'),
    (33, u'vampires'),
    (34, u'war'),
    (35, u'yaoi'),
    (36, u'yuri'),
]

USER_STATUS = [
    (0, 'none'),
    (1, 'want'),
    (2, 'now'),
    (3, 'ok'),
    (4, 'dropped'),
    (5, 'partially watched'),
]

class AnimeStudio(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title

class AnimeItem(models.Model):
    title = models.CharField(max_length=200, db_index=True, unique_for_date='releasedAt')
    genre = models.CommaSeparatedIntegerField(max_length=50, choices=ANIME_GENRE, blank=True)
    releaseType = models.IntegerField(choices=ANIME_TYPES)
    episodesCount = models.IntegerField()
    duration = models.IntegerField()
    releasedAt = models.DateTimeField()
    endedAt = models.DateTimeField()
    air = models.BooleanField()
    
    def __unicode__(self):
        return '%s [%s]' % (self.title, dict(ANIME_TYPES)[self.releaseType])
    
    class Meta:
        ordering = ["title"]

class AnimeEpisode(models.Model):
    title = models.CharField(max_length=200)
    anime = models.ForeignKey(AnimeItem)
    
    def __unicode__(self):
        return '%s [%s]' % (self.title, self.anime.title)

class AnimeName(models.Model):
    title = models.CharField(max_length=200)
    anime = models.ForeignKey(AnimeItem)

class AnimeForm(ModelForm):
    class Meta():
        model = AnimeItem
        exclude = ('air',)

class Credit(models.Model):
    title = models.CharField(max_length=200)
    
    def __unicode__(self):
        return '%s' % self.title
    
class Organisation(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return '%s' % self.title

class OrganisationBundle(models.Model):
    anime = models.ForeignKey(AnimeItem)
    organisation = models.ForeignKey(Organisation)
    job = models.ForeignKey(Credit)
    role = models.CharField(max_length=30)
    comment = models.CharField(max_length=100)

class People(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return '%s' % self.title

class PeopleBundle(models.Model):
    anime = models.ForeignKey(AnimeItem)
    person = models.ForeignKey(People)
    job = models.ForeignKey(Credit)
    role = models.CharField(max_length=30)
    comment = models.CharField(max_length=100)

class UserStatusBundle(models.Model):
    anime = models.ForeignKey(AnimeItem)
    user = models.ForeignKey(User)
    status = models.IntegerField(choices=USER_STATUS)
    count = models.IntegerField()
    changed = models.DateTimeField(auto_now=True)