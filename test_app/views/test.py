from django.http import HttpResponse
from django.core.mail import EmailMessage

from library.utils.pdf_booking import bukti_booking_pdf
from library.utils.send_notif import send_notif_admin

# Create your views here.

def sending_email(request):
    data = {
        'name': 'Daniardy Hilman',
        'email': 'dannyardi.danny@gmail.com',
        'user_partner': 'champion',
        'date_book': '17-01-2022',
        'court_title': 'Lapangan Futsal 2 Champion Tidar',
        'hours': '19:00 - 20:00',
        'price': 'Rp 100.000',
        'dp': 'Bayar DP',
        'id': '135'
    }

    buffer = bukti_booking_pdf(data)

    email = EmailMessage(
        'Kirim resi booking',
        'I love Django',
        to=['ahnafgibran@gmail.com'],
    )

    email.attach('Resi Booking.pdf', buffer.read())
    email.send()

    return HttpResponse('Your message has been sent')


def send_notif(request):
    req = send_notif_admin(12376)

    return HttpResponse(req)
