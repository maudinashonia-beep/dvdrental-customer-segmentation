from django.contrib import admin
from .models import ModelInfo, CustomerSegment
from django.utils.html import format_html
from django.utils.timezone import now
from django.urls import reverse

@admin.register(ModelInfo)
class ModelInfoAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'training_date', 'training_data', 'short_summary', 'retrain_button')
    search_fields = ('model_name', 'training_data')

    def short_summary(self, obj):
        return (obj.model_summary[:75] + '...') if obj.model_summary else "-"
    short_summary.short_description = "Summary"

    def retrain_button(self, obj):
        url = reverse('retrain_model', args=[obj.id])
        return format_html('<a class="button" href="{}">Retrain</a>', url)

    retrain_button.short_description = "Retrain"
    
    
#BARU

# Register your models here.
@admin.register(CustomerSegment)
class CustomerSegmentAdmin(admin.ModelAdmin):
    list_display = (
        'customer_id',
        'total_payment',
        'frequency',
        'cluster',
        'segment'
    )