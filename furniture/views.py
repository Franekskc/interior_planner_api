import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .firebase_client import FirebaseClient
from rest_framework import status
from rest_framework.views import APIView
from urllib.parse import parse_qs, urlparse
from .textures_config import FLOOR_TEXTURE_IDS, WALL_TEXTURE_IDS

class FurnitureListView(APIView):
    def get(self, request):
        client = FirebaseClient()
        furniture = client.get_all_furniture()
        
        transformed = [{
            'id': idx,
            'name': item.get('name'),
            'thumbnailUrl': item.get('thumbnail_url'),
        } for idx, item in enumerate(furniture)]

        return Response(transformed, status=status.HTTP_200_OK)

class FurnitureDetailView(APIView):
    def get(self, request, furniture_id):
        client = FirebaseClient()
        furniture = client.get_all_furniture()

        for idx, item in enumerate(furniture):
            if str(idx) == furniture_id:
                return Response({
                    "id": idx,
                    "name": item.get("name"),
                    "model_url": item.get("model_url"),
                    "thumbnail_url": item.get("thumbnail_url"),
                    "created_at": item.get("created_at").isoformat() if item.get("created_at") else None
                })

        return Response({"error": "Furniture not found"}, status=404)

class BaseTextureListView(APIView):
    ASSET_IDS = {}

    def get(self, request):
        results = []
        for asset_id in self.ASSET_IDS:
            url = f"https://ambientcg.com/api/v2/full_json?id={asset_id}"
            response = requests.get(url)
            if response.status_code != 200:
                continue

            data = response.json()
            asset = data.get("foundAssets", [{}])[0]
            preview = asset.get("previewImage", {})
            results.append({
                "id": asset.get("assetId"),
                "imageUrl": preview.get("256-JPG-FFFFFF")
            })
        return Response(results)


class BaseTextureDetailView(BaseTextureListView):
    ALLOWED_IDS = {}

    def get(self, request, texture_id):
        if texture_id not in self.ALLOWED_IDS:
            return Response({"error": "Not found"}, status=404)

        url = f"https://ambientcg.com/api/v2/full_json?id={texture_id}&include=downloadData"
        response = requests.get(url)
        if response.status_code != 200:
            return Response({"error": "Failed to fetch data"}, status=502)

        data = response.json()
        asset = data.get("foundAssets", [{}])[0]
        preview_links = asset.get("previewLinks", [])
        if not preview_links:
            return Response({"error": "Missing texture links"}, status=502)

        fragment = urlparse(preview_links[0]["url"]).fragment
        params = parse_qs(fragment)

        keys = {
            "color": "color_url",
            "displacement": "displacement_url",
            "normal": "normal_url",
            "roughness": "roughness_url",
            "ambientOcclusion": "ambientocclusion_url"
        }

        texture_data = {k: params.get(v, [""])[0] for k, v in keys.items()}
        return Response(texture_data)

# Walls
class WallTextureListView(BaseTextureListView):
    ASSET_IDS = WALL_TEXTURE_IDS

class WallTextureDetailView(BaseTextureDetailView):
    ALLOWED_IDS = WALL_TEXTURE_IDS


# Floors
class FloorTextureListView(BaseTextureListView):
    ASSET_IDS = FLOOR_TEXTURE_IDS

class FloorTextureDetailView(BaseTextureDetailView):
    ALLOWED_IDS = FLOOR_TEXTURE_IDS
