from django.db import models

# Create your models here.
class interns(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    salary=models.IntegerField(default=0)

    def __str__(self):
        return self.name