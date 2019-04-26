from django.contrib import admin
from .models import ItemBank

# Register your models here.


@admin.register(ItemBank)
class ItemBankAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'item_num',
        'item_type',
        'item_title',
        'item_a_anwser',
        'item_b_anwser',
        'item_c_anwser',
        'one_score_anwser',
        'tow_score_anwser',
        )

