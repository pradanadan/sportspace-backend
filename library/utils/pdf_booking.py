import io
from fpdf import FPDF
from django.http import FileResponse


def bukti_booking_pdf(data):
    buffer = io.BytesIO()

    pdf = FPDF('L', 'mm', (130, 210))
    pdf.add_page()
    pdf.set_margin(13)

    # Header
    pdf.image("media/pdf/logo.png", h=8, x=13, y=13)
    pdf.set_font('times', '', 12)
    pdf.cell(10, 3, '', ln=1)
    pdf.cell(115, 8, '')
    pdf.cell(15, 8, 'Nama')
    pdf.cell(3, 8, ':')
    pdf.cell(80, 8, data['name'], ln=1)
    pdf.cell(115, 8, '')
    pdf.cell(15, 8, 'Email')
    pdf.cell(3, 8, ':')
    pdf.cell(80, 8, data['email'], ln=1)

    # Body title
    pdf.set_font('times', 'B', 12)
    pdf.cell(10, 8, '', ln=1)
    pdf.cell(40, 8, 'Informasi Pemesanan', ln=1)
    pdf.set_font('times', '', 12)

    # First body line
    pdf.cell(2, 8, '')
    pdf.cell(30, 8, 'Nama Mitra')
    pdf.cell(3, 8, ':')
    pdf.cell(60, 8, data['user_partner'])
    pdf.cell(20, 8, '')
    pdf.cell(30, 8, 'Tanggal Booking')
    pdf.cell(3, 8, ':')
    pdf.cell(40, 8, data['date_book'], ln=1)

    # Second body line
    pdf.cell(2, 8, '')
    pdf.cell(30, 8, 'Judul Lapangan')
    pdf.cell(3, 8, ':')
    pdf.cell(60, 8, data['court_title'])
    pdf.cell(20, 8, '')
    pdf.cell(30, 8, 'Jam Booking')
    pdf.cell(3, 8, ':')
    pdf.cell(40, 8, data['hours'], ln=1)

    # Third body line
    pdf.cell(2, 8, '')
    pdf.cell(30, 8, 'Total Bayar')
    pdf.cell(3, 8, ':')
    pdf.cell(60, 8, data['price'])
    pdf.cell(20, 8, '')
    pdf.cell(30, 8, 'Pembayaran')
    pdf.cell(3, 8, ':')
    pdf.set_font('times', 'B', 12)
    pdf.cell(40, 8, data['dp'], ln=1)

    # Barcode
    pdf.interleaved2of5(data['id'], x=pdf.epw-22, y=pdf.eph, w=2, h=11)

    # Keterangan
    pdf.set_font('times', '', 11)
    pdf.cell(10, 37, '', ln=1)
    pdf.cell(40, 8, '*Tunjukan bentuk digital dokumen ini kepada petugas')


    pdf.output(buffer)
    buffer.seek(0)

    return buffer


def booking_file_download(request):
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
    return FileResponse(buffer, as_attachment=True, filename='bukti_booking.pdf')