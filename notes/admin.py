from django.contrib import admin
from .models import Note, Images

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
	class Meta:
		model = Note
		fields = '__all__'

class ImageAdmin(admin.ModelAdmin):
	class Meta:
		model = Images
		fields = '__all__'


admin.site.register(Note, NoteAdmin)
admin.site.register(Images, ImageAdmin)