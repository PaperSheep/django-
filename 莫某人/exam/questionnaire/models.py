from django.db import models

# Create your models here.
class ItemBank(models.Model):
    item_num = models.IntegerField()
    item_type = models.CharField(max_length=50, null=True) 
    item_title = models.CharField(max_length=50)
    item_a_anwser = models.CharField(max_length=50)
    item_b_anwser = models.CharField(max_length=50)
    item_c_anwser = models.CharField(max_length=50)
    one_score_anwser = models.CharField(max_length=50, null=True)
    tow_score_anwser = models.CharField(max_length=50, null=True)

