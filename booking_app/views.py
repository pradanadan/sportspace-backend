import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.parsers import MultiPartParser, FormParser

from library.models import Booking, Court, PaymentMethod, UserPartner, BookHoursDict, BookingHours, PaymentConfirm, BookingStatusCatalog
from library.utils.send_notif import send_notif_admin

class BookingView(APIView):
    def post(self, request, format=None):
        data = self.request.data

        try:
            d_user_partner = data['user_partner']
            slug = data['slug'] # Slug of court title
            date_book  = data['date_book'] # Format YYYY-MM-DD
            lunas = data['lunas'] # Boolean
            price = data['price']
            pMethod = data['pMethod'] # Code: 'bni', 'bri', 'mandiri', 'bca'
            hours = data['hours'] # Array {"hours": [{"start": "08:00", "end": "09:00"}, {"start": "09:00", "end":"10:00"}]}

            user = self.request.user
            user_partner = UserPartner.objects.get(username=d_user_partner)
            court = Court.objects.get(user_partner__username=d_user_partner, slug=slug)
            method = PaymentMethod.objects.get(code=pMethod)
            unique_price = price

            try:
                while True:
                    ran = random.randint(0,500)
                    unique_price = price + ran

                    qset= Booking.objects.filter(status__status_name="unpaid", unique_price=unique_price)

                    if qset.exists() != True:
                        break

                booking = Booking(user=user, user_partner=user_partner, court=court, date_book=date_book, 
                    lunas=lunas, price=price, unique_price=unique_price, method=method)
                booking.save()

                try:
                    for h in hours:
                        start = h['start']
                        end = h['end']

                        hours_dict = BookHoursDict.objects.get(hour_start=start, hour_end=end)
                        BookingHours.objects.create(booking_id=booking, book_hours=hours_dict)


                    return Response({"success": 1, "message" : "Booking order has been created", "booking_id": booking.id})

                except:
                    return Response({"success": 0, "message" : "Something went wrong when assigning booking hours"})

            except:
                return Response({"success": 0, "message" : "Something went wrong when creating booking order"})

        except:
            return Response({"success": 0, "message" : "Incomplete data"})


# Ajax request for booking detail
class PaymentCDSerializer(serializers.ModelSerializer):    
    pMethod = serializers.CharField(source='method.code')
    status = serializers.CharField(source='status.status_name')

    class Meta:
        model = Booking
        fields = ['unique_price', 'pMethod', 'status', 'active', 'payment_dl']


class PaymentCDView(APIView):
    def get(self, request, format=None):
        data = self.request.query_params

        try:
            user = self.request.user
            booking_id = data['booking_id']

            try:
                booking = Booking.objects.get(user=user, pk=booking_id)
                booking.cancellation()

                serializer = PaymentCDSerializer(booking)

                return Response(serializer.data)
            except:
                return Response({ 'error': 'Booking ID is invalid or the user has not permission' })
        except:
            return Response({ 'error': 'Data is incomplete' })


# Payment confirmation
class BookingHoursSerializer(serializers.ModelSerializer):
    start = serializers.TimeField(source='book_hours.hour_start', format='%H:%M')
    end = serializers.TimeField(source='book_hours.hour_end', format='%H:%M')

    class Meta:
        model = BookingHours
        fields = ['start', 'end']


class PCBookingSerializer(serializers.ModelSerializer):
    court_title = serializers.CharField(source='court.title')
    court_img = serializers.ImageField(source='court.img1')    
    court_type = serializers.CharField(source='court.type.name')
    court_address = serializers.CharField(source='court.user_partner.address')
    court_rate = serializers.IntegerField(source='court.rate')
    court_dp = serializers.IntegerField(source='court.dp')
    pMethod = serializers.CharField(source='method.code')
    hours = BookingHoursSerializer(many=True, read_only=True, source='bookinghours_set')

    class Meta:
        model = Booking
        # Rp 35.000 x2 jam
        fields = ['id', 'court_title', 'court_img', 'court_address','court_type', 'court_rate', 'court_dp', 'pMethod', 'lunas', 'price', 'unique_price', 'payment_dl', 'hours']


class PaymentConfirmSerializer(ModelSerializer):
    class Meta:
        model = PaymentConfirm
        fields = ['booking', 'bukti']

        def create(self, validated_data):
            return PaymentConfirm(**validated_data)


class PaymentConfirmView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        data = self.request.query_params

        try:
            user = self.request.user
            booking_id = data['booking_id']

            try:
                booking = Booking.objects.get(user=user, pk=booking_id)
                booking.cancellation()

                payment = PaymentConfirm.objects.filter(booking=booking)

                if booking.active:
                    serializer = PCBookingSerializer(booking)

                    jsonData = serializer.data
                    jsonData['unique_code'] = jsonData['unique_price'] - jsonData['price']

                    if jsonData['lunas']:
                        jsonData['kekurangan_harga'] = 0
                    else:
                        jsonData['kekurangan_harga'] = jsonData['court_rate'] - jsonData['price']

                    if payment.exists():
                        jsonData['first_upload'] = False

                        paymentSerializer = PaymentConfirmSerializer(payment[0])
                        jsonData['bukti'] = paymentSerializer.data['bukti']

                    else:
                        jsonData['first_upload'] = True

                    return Response(jsonData)
                else:
                    return Response({ 'error': 'Booking is inactive' })

            except:
                return Response({ 'error': 'Booking ID is invalid or the user has not permission' })
        except:
            return Response({ 'error': 'Data is incomplete' })


    def post(self, request, format=None):
        try:
            user = self.request.user
        
        except:
            return Response({ 'success': 0, 'message': 'User is not authenticated' })
        
        else:
            try:
                booking_id = request.data['booking']
                bukti = request.FILES['bukti']
            except:
                return Response({'success': 0, 'message': 'Data is incomplete'})
            else:
                try:
                    booking = Booking.objects.get(user=user, pk=booking_id)
                except:
                    return Response({'success': 0, 'message': 'Booking ID or user is not valid'})
                else:         
                    serializer = PaymentConfirmSerializer(data=request.data)

                    if serializer.is_valid():
                        serializer.save()

                        try:
                            status = BookingStatusCatalog.objects.get(status_name='paid_unconfirmed')
                            booking.status = status
                            booking.save()

                            notif = send_notif_admin(booking.unique_price)

                            print(notif)

                            return Response({ 'success': 1, 'message': 'Payment image has been uploaded' })
                        except:
                            return Response({'success': 0, 'message': 'Something happened when changing booking status'})                       
                    
                    else:
                        return Response({'success': 0, 'message': serializer.errors})

    def put(self, request, format=None):
        try:
            user = self.request.user
        
        except:
            return Response({ 'success': 0, 'message': 'User is not authenticated' })
        
        else:
            try:
                booking_id = request.data['booking']
                bukti = request.FILES['bukti']
            except:
                return Response({'success': 0, 'message': 'Data is incomplete'})
            else:
                try:
                    booking = Booking.objects.get(user=user, pk=booking_id)
                    payment = PaymentConfirm.objects.get(booking=booking)
                except:
                    return Response({'success': 0, 'message': 'Booking ID or user is not valid'})
                else:   
                    try:
                        payment.bukti.delete()      
                        payment.bukti = bukti
                        payment.save()
                        return Response({ 'success': 1, 'message': 'Payment receipt has been updated' })
                    except:
                        return Response({'success': 0, 'message': 'Something happened when changing payment receipt'})