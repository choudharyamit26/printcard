from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from weasyprint import HTML
from io import BytesIO
from django.core.files import File
from .models import Pdf
from .serializers import CardUrlSerializer, CreateBrochureOrLetterHeadSerializer


class CreatePdf(APIView):
    model = Pdf
    serializer_class = CardUrlSerializer

    def post(self, request, *args, **kwargs):
        # front_image_url = self.request.data['front_image_url']
        # back_image_url = self.request.data['back_image_url']
        # no_of_cards = self.request.data['no_of_cards']
        # front_image_url = 'https://petparenting-node.s3.ap-south-1.amazonaws.com/order/1608206645946-file.jpeg'
        # back_image_url = 'https://petparenting-node.s3.ap-south-1.amazonaws.com/order/1608206644607-file.jpeg'
        # no_of_cards = 37
        # print(no_of_cards // 10)
        # print(no_of_cards % 10)
        serializer = CardUrlSerializer(data=self.request.data)
        # print(self.request.data['front_image_url'])
        # print(self.request.data['back_image_url'])
        if serializer.is_valid():
            context = {
                'front_image_url': serializer.validated_data['front_image_url'],
                'back_image_url': serializer.validated_data['back_image_url'],
                'no_of_cards': range(0, int(serializer.validated_data['no_of_cards']) // 10),
                'remainder': range(0, int(serializer.validated_data['no_of_cards']) % 10)
            }
            # return render(self.request, 'index.html', context)
            html_string = render_to_string('index.html', context)
            html = HTML(string=html_string)
            result = html.write_pdf()
            x = HttpResponse(result, content_type='application/pdf')
            filename = "Order.pdf"
            y = self.model.objects.create(order_id=1)
            if request.is_secure():
                protocol = "https"
            else:
                protocol = "http"
            domain = request.META['HTTP_HOST']
            y.pdf.save(filename, File(BytesIO(x.content)))
            complete_url = protocol + '://' + domain + y.pdf.url
            print(complete_url)
            return Response({"url": complete_url, "status": HTTP_200_OK})
            # return Response(serializer.data)
        else:
            return Response({"message": serializer.errors, "status": HTTP_400_BAD_REQUEST})


class CreateBrochureOrLetterHead(APIView):
    model = Pdf
    serializer_class = CreateBrochureOrLetterHeadSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateBrochureOrLetterHeadSerializer(data=self.request.data)
        if serializer.is_valid():
            print(int(serializer.validated_data['page_count'])//2)
            context = {
                'front_image_url': serializer.validated_data['front_image_url'],
                'back_image_url': serializer.validated_data['back_image_url'],
                'page_count': range(0, int(serializer.validated_data['page_count'])//2)
            }
            html_string = render_to_string('index2.html', context)
            html = HTML(string=html_string)
            result = html.write_pdf()
            x = HttpResponse(result, content_type='application/pdf')
            filename = "Order.pdf"
            y = self.model.objects.create(order_id=1)
            if request.is_secure():
                protocol = "https"
            else:
                protocol = "http"
            domain = request.META['HTTP_HOST']
            y.pdf.save(filename, File(BytesIO(x.content)))
            complete_url = protocol + '://' + domain + y.pdf.url
            print(complete_url)
            return Response({'url': complete_url, 'status': HTTP_200_OK})
            # return render(self.request, 'index2.html', context)
        else:
            return Response({'message': serializer.errors, 'status': HTTP_400_BAD_REQUEST})


class CreatePdfViewSet(viewsets.ModelViewSet):
    queryset = Pdf.objects.all()
    serializer_class = CardUrlSerializer
