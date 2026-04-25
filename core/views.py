from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import ReferencePhoto

def get_coordinates(request, file_name):   
    try: 
        photo = ReferencePhoto.objects.get(image__icontains=file_name)

        return JsonResponse({
            "status": "success",
            "data": {
                "location": photo.location.name, 
                "x": photo.x_coord, 
                "y": photo.y_coord,
                "z": photo.z_coord,
                "floor": photo.floor,
                "description": photo.description,
            }
        })
    except ReferencePhoto.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": f"No reference photo found for file: {file_name}"
        }, status=404)