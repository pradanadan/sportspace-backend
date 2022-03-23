import textwrap

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import permissions
from django.core.mail import EmailMessage

from library.models import PaymentConfirm, Booking, BookingHours, BookingStatusCatalog
from library.utils.pdf_booking import bukti_booking_pdf


# Serializer for Payment List
class PaymentConfirmSerializer(serializers.ModelSerializer):
    booking_id = serializers.CharField(source='booking.id')
    price = serializers.CharField(source='booking.price')
    unique_price = serializers.CharField(source='booking.unique_price')
    pMethod = serializers.CharField(source='booking.method.code')

    class Meta:
        model = PaymentConfirm
        fields = ['booking_id', 'unique_price', 'pMethod', 'bukti', 'price']


class PaymentConfirmList(APIView):
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request, format=None):
        books = PaymentConfirm.objects.filter(read=False).order_by('pk')

        serializer = PaymentConfirmSerializer(books, many=True)
        
        return Response(serializer.data)

# Serializer for Booking Detail
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
    user = serializers.CharField(source='user.email')

    class Meta:
        model = Booking
        fields = ['id', 'status', 'user', 'court_title', 'court_img', 'court_address', 'court_type', 'user_partner', 'slug', 'price', 'unique_price', 'date_book', 'hours']


class BookingDetail(APIView):
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request, format=None):
        booking_id = request.query_params['booking_id']
        booking = Booking.objects.get(pk=booking_id)

        serializer = BookingSerializer(booking)
        
        return Response(serializer.data)

# Payment validation
class PaymentValidationView(APIView):
    permission_classes = (permissions.IsAdminUser, )

    def put(self, request, format=None):
        try:
            booking_id = request.data['booking_id']
            accept = request.data['accept']
        except:
            return Response({ 'success': 0, 'message': 'Data is incomplete' })
        
        else:
            try:
                booking = Booking.objects.get(pk=booking_id)
                payment = PaymentConfirm.objects.get(booking=booking)

            except:
                return Response({ 'success': 0, 'message': 'Booking ID is invalid' })
            
            else:
                # if payment accepted
                if accept:
                    status = BookingStatusCatalog.objects.get(status_name='paid')
                    booking.status = status
                    booking.save()

                    payment.read = True
                    payment.save()

                    success = True
                    SendEmail(booking, success)

                    if success:
                        return Response({ 'success': 1, 'message': 'Payment has been accepted and email has been sent' })
                    else:
                        return Response({ 'success': 0, 'message': 'Something wrong happened when sending email' })

                # if payment rejected
                else:
                    status = BookingStatusCatalog.objects.get(status_name='payment_rejected')
                    booking.status = status
                    booking.save()

                    payment.read = True
                    payment.save()

                    return Response({ 'success': 1, 'message': 'Payment has been rejected' })

# Send receipt to email
class SendBookingReceipt(APIView):
    permission_classes = (permissions.IsAdminUser, )

    def post(self, request, format=None):
        try:
            booking_id = request.data['booking_id']
        
        except:
            return Response({ 'success': 0, 'message': 'Data is incomplete' })
        
        else:
            try:
                booking = Booking.objects.get(pk=booking_id, status__status_name='paid')
            except:
                return Response({ 'success': 0, 'message': 'Booking ID is invalid or unpaid' })
            else:
                success = True
                SendEmail(booking, success)

                if success:
                    return Response({ 'success': 1, 'message': 'Email has been sent' })
                else:
                    return Response({ 'success': 0, 'message': 'Something wrong happened when sending email' })

    
def SendEmail(booking, success):
    try:
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

        message = EmailMessage(
            'Resi Booking',
            'Terimakasih telah melakukan pemesanan lapangan olahraga dengan jasa kami. Berikut adalah resi booking Anda.',
            to=[email],
        )

        message.attach('Resi Booking.pdf', buffer.read())
        message.send()

        success = True

    except:
        success = False
