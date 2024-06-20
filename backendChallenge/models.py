from django.db import models

class ExchangeRate(models.Model):
    date = models.DateField()
    rate = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f"{self.date} - {self.rate}"
