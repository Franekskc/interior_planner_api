import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .firebase_client import FirebaseClient
from rest_framework import status
from rest_framework.views import APIView
from urllib.parse import parse_qs, urlparse

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

class BaseTextureListView(APIView):
    ASSET_IDS = []

    def get_texture_data(self, asset_id):
        url = f"https://ambientcg.com/api/v2/full_json?id={asset_id}&include=downloadData"
        response = requests.get(url)
        if response.status_code != 200:
            return None

        data = response.json()
        if not data.get("foundAssets"):
            return None

        asset = data["foundAssets"][0]
        preview = asset.get("previewImage", {})
        texture_links = self.extract_texture_links(asset)

        return {
            "id": asset["assetId"].lower(),
            "imageUrl": preview.get("256-JPG-FFFFFF"),
            "texture": texture_links
        }

    def extract_texture_links(self, asset):
        preview_links = asset.get("previewLinks", [])
        if not preview_links:
            return {}

        query = urlparse(preview_links[0]["url"]).fragment
        params = parse_qs(query)
        keys = ["color", "displacement", "normal", "roughness", "ambientocclusion"]
        result = {}
        for key in keys:
            result[key] = params.get(f"{key}_url", [""])[0]
        return result

    def get(self, request):
        results = []
        for asset_id in self.ASSET_IDS:
            texture_data = self.get_texture_data(asset_id)
            if texture_data:
                results.append(texture_data)
        return Response(results)


class WallTextureListView(BaseTextureListView):
    ASSET_IDS = [
        "Plaster001",
    ]


class FloorTextureListView(BaseTextureListView):
    ASSET_IDS = [
        "PavingStones147",
        "WoodFloor049",
    ]
