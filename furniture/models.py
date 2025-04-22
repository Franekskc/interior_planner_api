from django.db import models
from django.utils.text import slugify
from firebase_admin import firestore, storage
import logging
import os

logger = logging.getLogger(__name__)

class Furniture(models.Model):
    name = models.CharField(max_length=100, unique=True)
    model_3d = models.FileField(upload_to='local_models/')
    thumbnail = models.ImageField(upload_to='local_thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    firebase_model_url = models.URLField(blank=True)
    firebase_thumbnail_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        
        super().save(*args, **kwargs)
        
        if is_new:
            self._upload_to_firebase()
            self._create_firestore_document()
            os.remove(self.model_3d.path)
            os.remove(self.thumbnail.path)

    def _upload_to_firebase(self):
        """Uploads files to a Firebase Storage with proper names."""
        sanitized = slugify(self.name)
        bucket = storage.bucket()

        try:
            # Send 3D model
            model_blob = bucket.blob(f'models/{sanitized}.glb')
            with open(self.model_3d.path, 'rb') as model_file:
                model_blob.upload_from_file(model_file)
                model_blob.make_public()
            
            # Send thumbnail
            thumb_blob = bucket.blob(f'thumbnails/{sanitized}.jpg')
            with open(self.thumbnail.path, 'rb') as thumb_file:
                thumb_blob.upload_from_file(thumb_file)
                thumb_blob.make_public()

            # Update URLs
            self.firebase_model_url = model_blob.public_url
            self.firebase_thumbnail_url = thumb_blob.public_url
            super().save(update_fields=['firebase_model_url', 'firebase_thumbnail_url'])

        except Exception as e:
            logger.error(f"Error uploading files to Firebase: {str(e)}")
            self.delete()
            raise

    def _create_firestore_document(self):
        """Create document in Firestore"""
        sanitized = slugify(self.name)
        try:
            doc_ref = firestore.client().collection('furniture').document(sanitized)
            doc_ref.set({
                'name': self.name,
                'model_url': self.firebase_model_url,
                'thumbnail_url': self.firebase_thumbnail_url,
                'created_at': firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            logger.error(f"Error Firestore: {str(e)}")
            raise

    def __str__(self):
        return self.name