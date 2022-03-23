from django.http import JsonResponse
from rest_framework import serializers

from library.models.court import *
from library.models.article import *


# Ajax request for recomendation 1 & 2
class CourtSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='user_partner.address')
    city = serializers.CharField(source='user_partner.city')
    type = serializers.CharField(source='type.name')
    user_partner = serializers.CharField(source='user_partner.username')
    
    class Meta:
        model = Court
        fields = ['title', 'type', 'rate', 'address', 'city', 'img1', 'user_partner', 'slug']

def get_rec_1(request):
    courts = Court.objects.order_by('title')[:15]
    
    serializer = CourtSerializer(courts, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_rec_2(request):
    courts = Court.objects.order_by('-pk')[:15]
    
    serializer = CourtSerializer(courts, many=True)
    return JsonResponse(serializer.data, safe=False)


# Ajax request for articles
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'preview_text', 'preview_img']

def get_article(request):
    article = Article.objects.order_by('-pk')[:2]
    
    serializer = ArticleSerializer(article, many=True)
    return JsonResponse(serializer.data, safe=False)