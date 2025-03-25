from firebase_admin import firestore
import logging

logger = logging.getLogger(__name__)

class FirebaseClient:
    def __init__(self):
        self.db = firestore.client()
        self.collection = 'furniture'

    def get_all_furniture(self):
        try:
            docs = self.db.collection(self.collection).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            logger.error(f"Firestore error: {str(e)}")
            return []