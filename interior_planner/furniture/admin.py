from django.contrib import admin
from .models import Furniture
from django.utils.html import format_html
from django.utils.text import slugify
import os

@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('created_at',)
    
    def firebase_links(self, obj):
        sanitized = slugify(obj.name)
        return format_html(
            '<strong>Firestore:</strong> <a href="https://console.firebase.google.com/project/_/firestore/data/~2Ffurniture~2F{sanitized}">Document</a><br>'
            '<strong>3D Model:</strong> <a href="https://storage.googleapis.com/{bucket}/models/{sanitized}.glb">Download</a><br>'
            '<strong>Thumbnail:</strong> <a href="https://storage.googleapis.com/{bucket}/thumbnails/{sanitized}.jpg">View</a>',
            sanitized=sanitized,
            bucket=os.getenv('FIREBASE_STORAGE_BUCKET')
        )
    firebase_links.short_description = "Firebase Links"