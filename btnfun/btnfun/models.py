from django.db import models

class Number(models.Model):
    number = models.IntegerField(default=0)

    def __str__(self):
        return str(self.number)

    class Meta:
        db_table = "number"