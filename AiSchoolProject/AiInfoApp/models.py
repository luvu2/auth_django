from django.db import models

# Create your models here.
class AiClass(models.Model):
    class_num = models.IntegerField()
    teacher = models.CharField(max_length=10)
    class_room = models.CharField(max_length=10)


class AiStudent(models.Model):
    class_num = models.IntegerField()
    name = models.CharField(max_length=10)
    phone_num = models.CharField(max_length=10)
    intro = models.TextField()