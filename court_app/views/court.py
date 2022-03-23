from rest_framework import serializers
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from library.models.court import *
from library.models.booking import *

# Ajax request for court detail
class CourtSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='user_partner.address')
    city = serializers.CharField(source='user_partner.city')
    kecamatan = serializers.CharField(source='user_partner.kecamatan')
    longitude = serializers.DecimalField(source='user_partner.longitude', max_digits=11, decimal_places=6)
    latitude = serializers.DecimalField(source='user_partner.latitude', max_digits=11, decimal_places=6)
    type = serializers.CharField(source='type.name')
    user_partner = serializers.CharField(source='user_partner.username')
    
    class Meta:
        model = Court
        fields = ['title', 'type', 'rate', 'dp', 'address', 'kecamatan', 'city', 'longitude', 
            'latitude', 'room', 'floor', 'loker', 'ruang_ganti', 'shower_room', 'deskripsi',
            'img1', 'img2', 'img3', 'img4', 'img5', 'img6', 'img7', 'img8', 'img9', 'img10', 
            'user_partner', 'slug']

class CourtDetailView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None, *args, **kwargs):
        user_partner = kwargs['user_partner']
        slug = kwargs['slug']

        court = Court.objects.get(user_partner__username=user_partner, slug=slug)

        serializer = CourtSerializer(court)
        data = serializer.data

        if request.user.is_authenticated:
            user = request.user

            if FavCourt.objects.filter(user=user, court=court).exists():
                data['favorite'] = True
            else:
                data['favorite'] = False

        return Response(data)


# Class for hours result in date checking
class op_hour():
    def __init__(self, start, end, available):
        self.start = start
        self.end = end
        self.available = available


class OpHoursSerializer(serializers.Serializer):
    start = serializers.TimeField()
    end = serializers.TimeField()
    available = serializers.BooleanField()


def check(request, user_partner, slug):

    if request.method == 'GET':
        date = request.GET.get('date')
        results = []

        book_hours = BookingHours.objects.filter(
            booking_id__date_book=date).filter(
            booking_id__court__user_partner__username=user_partner,
            booking_id__court__slug=slug).exclude(booking_id__active=False)

        partner = UserPartner.objects.get(username=user_partner)
        op_hour_start = partner.op_hours_start
        op_hour_end = partner.op_hours_end

        op_hours = BookHoursDict.objects.filter(hour_start__gte=op_hour_start, hour_end__lte=op_hour_end)

        for op in op_hours:
            available = True

            for b in book_hours:
                if op.hour_start == b.book_hours.hour_start:
                    available = False

            results.append(op_hour(op.hour_start, op.hour_end, available))

        serializer = OpHoursSerializer(results, many=True)
        return JsonResponse(serializer.data, safe=False)
