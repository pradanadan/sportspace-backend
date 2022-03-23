from datetime import datetime
from django.http import FileResponse
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
import textwrap

from library.models import Booking, BookingHours
from library.utils.pdf_booking import bukti_booking_pdf


# Serializer for Booking and BookingHours
class BookingHoursSerializer(serializers.ModelSerializer):
    start = serializers.TimeField(source='book_hours.hour_start', format='%H:%M')
    end = serializers.TimeField(source='book_hours.hour_end', format='%H:%M')

    class Meta:
        model = BookingHours
        fields = ['start', 'end']

class BookingSerializer(serializers.ModelSerializer):
    court_title = serializers.CharField(source='court.title')
    court_img = serializers.ImageField(source='court.img1')    
    court_type = serializers.CharField(source='court.type.name')
    user_partner = serializers.CharField(source='court.user_partner.username')
    court_address = serializers.CharField(source='court.user_partner.address')
    hours = BookingHoursSerializer(many=True, read_only=True, source='bookinghours_set')
    date_book = serializers.DateField(format='%d-%m-%Y')
    slug = serializers.SlugField(source='court.slug')
    status = serializers.CharField(source='status.status_name')

    class Meta:
        model = Booking
        fields = ['status', 'court_title', 'court_img', 'court_address', 'user_partner','court_type', 'slug', 'id', 'unique_price', 'date_book', 'hours', 'payment_dl']


class MyBills(APIView):
    def get(self, request, format=None):
        user = request.user

        now = datetime.now() 
        books = Booking.objects.filter(user=user, active=True).filter(
            (Q(payment_dl__gt=now) & Q(status__status_name='unpaid')) | Q(status__status_name='paid_unconfirmed')).order_by('-pk')

        serializer = BookingSerializer(books, many=True)
        
        return Response(serializer.data)


class MyBooking(APIView):
    def get(self, request, format=None):
        user = request.user

        now = datetime.now() 
        books = Booking.objects.filter(user=user, active=True).filter(
            date_book__gte=now).exclude(
                Q(status__status_name='unpaid') | Q(status__status_name='paid_unconfirmed')).order_by('-pk')

        serializer = BookingSerializer(books, many=True)
        
        return Response(serializer.data)


class OrderHistory(APIView):
    def get(self, request, format=None):
        user = request.user

        now = datetime.now() 
        books = Booking.objects.filter(user=user, active=True).filter(
            date_book__lt=now).exclude(
                Q(status__status_name='unpaid') | Q(status__status_name='paid_unconfirmed')).order_by('-pk')

        serializer = BookingSerializer(books, many=True)
        
        return Response(serializer.data)


class GetBookingReceipt(APIView):
    def get(self, request, format=None):
        user = request.user
        booking_id = request.query_params['booking_id']

        try:
            booking = Booking.objects.get(pk=booking_id, user=user, status__status_name='paid')

        except:
            return Response({'error': 'Booking ID or user is invalid'})
        
        else:
            if booking.user.name:
                name = booking.user.name
            else:
                name = ''
                
            email = booking.user.email
            user_partner = booking.user_partner.venue_name
            date_book = booking.date_book.strftime('%d-%m-%Y')

            court_title = booking.court.title
            court_title = textwrap.shorten(court_title, width=40, placeholder='...')

            price = 'Rp ' + f'{booking.price:n}'
            barcode = str(booking.id)

            if booking.lunas:
                dp = 'Lunas'
            else:
                dp = 'Bayar DP'

            first_hours = BookingHours.objects.filter(booking_id=booking).first()
            last_hours = BookingHours.objects.filter(booking_id=booking).last()

            hours = first_hours.book_hours.hour_start.strftime('%H:%M')
            hours += ' - ' + last_hours.book_hours.hour_end.strftime('%H:%M')

            data = {
                'name': name,
                'email': email,
                'user_partner': user_partner,
                'date_book': date_book,
                'court_title': court_title,
                'hours': hours,
                'price': price,
                'dp': dp,
                'id': barcode
            }

            buffer = bukti_booking_pdf(data)
            return FileResponse(buffer, as_attachment=True, filename='Resi Booking.pdf')
        
           
