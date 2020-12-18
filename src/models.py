from django.db import models


class Pdf(models.Model):
    order_id = models.IntegerField()
    pdf = models.FileField()
