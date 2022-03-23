import locale

from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import serializers

from library.models.court import *
from library.models.booking import *


# Ajax request for search result
class CourtSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='user_partner.address')
    city = serializers.CharField(source='user_partner.city')
    type = serializers.CharField(source='type.name')
    user_partner = serializers.CharField(source='user_partner.username')
    longitude = serializers.CharField(source='user_partner.longitude')
    latitude = serializers.CharField(source='user_partner.latitude')
    
    class Meta:
        model = Court
        fields = ['title', 'type', 'rate', 'address', 'city', 'img1', 'user_partner', 'slug', 'longitude', 'latitude']
        

def search(request):
    if request.method == 'GET':
        courts = Court.objects.all()

        key = request.GET.get('key')
        type = request.GET.get('type')
        date = request.GET.get('date')
        hour_start = request.GET.get('hour_start')
        hour_end = request.GET.get('hour_end')
        rate_min = request.GET.get('rate_min')
        rate_max = request.GET.get('rate_max')

        if key:            
            keys = key.split()

            if 'di' in keys: keys.remove('di')

            for k in range(len(keys)):
                if k == 0:
                    courts = courts.filter(
                        Q(title__icontains=keys[k]) | 
                        Q(type__code__icontains=keys[k]) |
                        Q(user_partner__address__icontains=keys[k]) |
                        Q(user_partner__kecamatan__name__icontains=keys[k]) |
                        Q(user_partner__city__city__icontains=keys[k]) |
                        Q(user_partner__venue_name__icontains=keys[k])
                        )
                
                else:
                    courts = courts.filter(
                        Q(title__icontains=keys[k]) | 
                        Q(type__code__icontains=keys[k]) |
                        Q(user_partner__address__icontains=keys[k]) |
                        Q(user_partner__kecamatan__name__icontains=keys[k]) |
                        Q(user_partner__city__city__icontains=keys[k]) |
                        Q(user_partner__venue_name__icontains=keys[k])
                        )
        
        if type:
            courts = courts.filter(type__code=type)
        
        if date and hour_start and hour_end:
            booking = Booking.objects.filter(Q(date_book=date) & 
                ( Q(bookinghours__book_hours__hour_start__gte=hour_start) & 
                Q(bookinghours__book_hours__hour_end__lte=hour_end) )).exclude(active=False)

            for b in booking:
                courts = courts.exclude(booking__pk=b.id)
        
        if rate_max:
            courts = courts.filter(rate__lte=rate_max)
        
        if rate_min:
            courts = courts.filter(rate__gte=rate_min)
            
        courts = courts.order_by('n_book')[:20]

    serializer = CourtSerializer(courts, many=True)
    return JsonResponse(serializer.data, safe=False)
