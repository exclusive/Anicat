
from django.contrib import auth
from django.core.cache import cache
from django.db.models import Q
from anime.forms.Error import UploadMalListForm
from anime.forms.User import UserCreationFormMail, NotActiveAuthenticationForm
from anime.malconvert import passFile
from anime.models import AnimeRequest
from datetime import datetime, timedelta

def login(request):
    response = {}
    form = None
    if request.method != 'POST':
        response['text'] = 'Only POST method allowed.'
    elif request.user.is_authenticated():
        response['text'] = 'Already logged in.'
    else:
        form = NotActiveAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            response.update({'response': True,
                'text': {'name': user.username}})
    response['form'] = form or NotActiveAuthenticationForm()
    return response

def register(request):
    response = {}
    form = None
    if request.method != 'POST':
        response['text'] = 'Only POST method allowed.'
    elif request.user.is_authenticated():
        response['text'] = 'Already registred.'
    else:
        form = UserCreationFormMail(request.POST)
        if form.is_valid():
            user = form.save()
            user = auth.authenticate(username=user.username, password=form.cleaned_data['password1'])
            auth.login(request, user)
            response.update({'response': True, 'text': {'name': user.username}})
    response['form'] = form or UserCreationFormMail()
    return response

def loadMalList(request):
    lastLoad = cache.get('MalList:%s' % request.user.id)
    if request.method == 'POST':
        form = UploadMalListForm(request.POST, request.FILES)
        if form.is_valid():
            timeLeft = 0
            try:
                timeLeft = (1800 - (datetime.now() - lastLoad['date']).seconds) / 60
            except TypeError:
                lastLoad = {}
                pass
            if lastLoad and timeLeft > 0:
                form.addError('You doing it too often. Try again in %s minutes.' % timeLeft)
            else:
                status, error = passFile(request.FILES['file'],
                        request.user, form.cleaned_data['rewrite'])
                if not status:
                    form.addError(error)
                else:
                    lastLoad['updated'] = True
    else:
        form = UploadMalListForm()
    return {'mallistform': form, 'mallist': lastLoad}

def getRequests(user, *keys):
    try:
        qs = AnimeRequest.objects.filter(user=user).order_by('status', '-id')
        qs = qs.exclude(Q(status__gt=2) & Q(changed__lte=datetime.now()-timedelta(days=20)))
        c = qs.filter(status__gt=2).count()
        if c > 20:
            qs = qs[:qs.count() - (c - 10)]
        if keys:
            qs = qs.values(*keys)
        try:
            types = AnimeRequest._meta.get_field('requestType').choices
        except:
            pass
        return {'requests': list(qs),
                'requestTypes': types}
    except:
        pass
