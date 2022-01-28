from django.contrib import admin
from .models import kvvk ,Documents , Exam
# Register your models here.




class KVKKAdmin(admin.ModelAdmin):
    list_display = ['name']



class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name']

class ExamAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(kvvk,KVKKAdmin)
admin.site.register(Exam,ExamAdmin)
admin.site.register(Documents,DocumentAdmin)