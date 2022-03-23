import locale
from django.http import HttpResponse
from django.template import loader

from library.models.court import *
from library.models.article import *

locale.setlocale(locale.LC_ALL, '')

def home(request):
    courts_1 = Court.objects.order_by('title')[:15]
    courts_2 = Court.objects.order_by('-pk')[:15]
    articles = Article.objects.order_by('-pk')[:2]

    for court in courts_1:
        court.rate = f'{court.rate:n}'
    for court in courts_2:
        court.rate = f'{court.rate:n}'

    template = loader.get_template('test_app/home/home.html')
    context = {
        'recomendation_1': courts_1,
        'recomendation_2': courts_2,
        'articles': articles,
    }

    return HttpResponse(template.render(context, request))