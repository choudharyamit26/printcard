from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from weasyprint import HTML
from io import BytesIO
from django.core.files import File
from .models import Pdf


class CreatePdf(APIView):
    model = Pdf

    def post(self, request, *args, **kwargs):
        front_image_url = self.request.data['front_image_url']
        back_image_url = self.request.data['back_image_url']
        no_of_cards = self.request.data['no_of_cards']
        # front_image_url = 'https://petparenting-node.s3.ap-south-1.amazonaws.com/order/1608206645946-file.jpeg'
        # back_image_url = 'https://petparenting-node.s3.ap-south-1.amazonaws.com/order/1608206644607-file.jpeg'
        # no_of_cards = 37
        # print(no_of_cards // 10)
        # print(no_of_cards % 10)
        context = {
            'front_image_url': front_image_url,
            'back_image_url': back_image_url,
            'no_of_cards': range(0, int(no_of_cards) // 10),
            'remainder': range(0, int(no_of_cards) % 10)
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
