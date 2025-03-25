from rest_framework.decorators import api_view
from rest_framework.response import Response
from .firebase_client import FirebaseClient
from rest_framework import status

@api_view(['GET'])
def furniture_list(request):
    client = FirebaseClient()
    furniture = client.get_all_furniture()
    
    # Transform data for frontend
    transformed = [{
        'id': idx,
        'name': item.get('name'),
        'model_url': item.get('model_url'),
        'thumbnail_url': item.get('thumbnail_url'),
        'created_at': item.get('created_at').isoformat() if item.get('created_at') else None
    } for idx, item in enumerate(furniture)]
    
    return Response(transformed, status=status.HTTP_200_OK)