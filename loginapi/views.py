from django.shortcuts import render
from rest_framework import viewsets
from .models import Userverification
from .serializers import UserVerificationSerializer
import csv,io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from PyPDF2 import PdfFileWriter,PdfFileReader
from rest_framework.decorators import action
from django.conf import settings
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.pdfmetrics import stringWidth
# Create your views here.

class UserVerificationViewset(viewsets.ModelViewSet):
    queryset = Userverification.objects.all()
    serializer_class = UserVerificationSerializer
    @action(methods=['POST'],detail=True)
    def posting(self, request):
        print(request)
        email = request.data['email']
        with open(str(settings.BASE_DIR)+'\loginapi\lib\CodeCombatLeaderboard.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            name=None
            contest_name=None
            for row in csv_reader:
                print(row[1])
                print(email)
                if row[1] == email:
                    print(row[1])
                    login = True
                    contest_name=row[4]
                    name=row[0]
                    break
                else:
                    print(row[1])
                    login = False
                    continue

            if login == True:
                print('successfully logged in')
                packet = io.BytesIO()
                packet1 = io.BytesIO()
                packet2 = io.BytesIO()
                packet3 = io.BytesIO()
                packet4 = io.BytesIO()
                packet5 = io.BytesIO()
                BOLD = '\033[1m'
                END = '\033[0m'
                PAGE_WIDTH = defaultPageSize[0]
                # create a new PDF with Reportlab
                can = canvas.Canvas(packet, pagesize=letter)
                can.setFillColor(colors.HexColor('#4678BD'))
                can.setFont("Times-Roman",30)
                text_width0=stringWidth('This is to ceritfy that has actively','Times-Bold',30)
                if len(name.split(' '))>1:
                    nam=name.split(' ')[0]
                else:
                    nam=name
                can.drawString((PAGE_WIDTH - text_width0)+20, 293, 'This is to certify that')
                can.save()
                can1=canvas.Canvas(packet1,pagesize=letter)
                can1.setFillColor(colors.HexColor('#4678BD'))
                can1.setFont("Times-Roman",30)
                #text_width1 = stringWidth('has actively participated in '+contest_name+' held','Times-Bold',30)
                can1.drawString(255,257,'has actively participated in ')
                can1.save()
                can2 = canvas.Canvas(packet2, pagesize=letter)
                can2.setFillColor(colors.HexColor('#4678BD'))
                can2.setFont("Times-Roman", 30)
                text_width2 = stringWidth('on 03/10/2020, organized by IEEE-BPIT Student Branch in','Times-Bold',30)
                can2.drawString(170, 215, 'Webinar on Growth Hacks for LinkedIn ')
                can2.save()
                can3 = canvas.Canvas(packet3, pagesize=letter)
                can3.setFillColor(colors.HexColor('#4678BD'))
                can3.setFont("Times-Roman", 30)
                text_width3 = stringWidth('in association with Educative.','Times-Bold',30)
                can3.drawString(50, 180, 'held on 03/10/2020, organized by IEEE-BPIT Student Branch')
                can3.save()
                can4 = canvas.Canvas(packet4, pagesize=letter)
                can4.setFillColor(colors.HexColor('#4678BD'))
                can4.setFont("Times-Bold", 30)
                text_width4 = stringWidth('in association with Educative.', 'Times-Bold', 30)
                can4.drawString((PAGE_WIDTH - text_width0)+285, 293, nam)
                can4.save()
                can5 = canvas.Canvas(packet5, pagesize=letter)
                can5.setFillColor(colors.HexColor('#4678BD'))
                can5.setFont("Times-Roman", 30)
                text_width5 = stringWidth('in association with Educative.', 'Times-Bold', 30)
                can5.drawString(190, 145,'in association with Edudictive Pvt. Ltd.')
                can5.save()


                # move to the beginning of the StringIO buffer
                packet.seek(0)
                new_pdf = PdfFileReader(packet)
                packet1.seek(0)
                new_pdf1 = PdfFileReader(packet1)
                packet2.seek(0)
                new_pdf2= PdfFileReader(packet2)
                packet3.seek(0)
                new_pdf3 = PdfFileReader(packet3)
                packet4.seek(0)
                new_pdf4 = PdfFileReader(packet4)
                packet5.seek(0)
                new_pdf5 = PdfFileReader(packet5)
                # read your existing PDF
                existing_pdf = PdfFileReader(open(str(settings.BASE_DIR)+"\loginapi\lib\certi.pdf", "rb"))
                print('DIR:- '+settings.BASE_DIR)
                output = PdfFileWriter()
                # add the "watermark" (which is the new pdf) on the existing page
                page = existing_pdf.getPage(0)
                page.mergePage(new_pdf.getPage(0))
                page.mergePage(new_pdf1.getPage(0))
                page.mergePage(new_pdf2.getPage(0))
                page.mergePage(new_pdf3.getPage(0))
                page.mergePage(new_pdf4.getPage(0))
                page.mergePage(new_pdf5.getPage(0))
                output.addPage(page)
                print('yahan tak theek h ')
                outputStream=open(str(settings.BASE_DIR)+"\loginapi\lib\q"+name,'wb')
                print('yahan margya')
                print(outputStream)
                output.write(outputStream)
                print('yahan margya 1')
                outputStream.close()
                print('yahan margya 2')
                outputStream=open(str(settings.BASE_DIR)+"\loginapi\lib\q"+name,'rb')
                Response=HttpResponse(FileWrapper(outputStream),content_type='application/pdf')
                return Response
