from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from shortener.models import ShortenedURL, AdGallery
from shortener.api.serializers import URLShortenSerializer

class CreateShortURL(APIView):
    def post(self, request, *args, **kwargs):
        serializer = URLShortenSerializer(data=request.data)
        if serializer.is_valid():
            short_url = serializer.save()
            return Response({
                'short_url': f"{request.build_absolute_uri('/')}{short_url.short_code}/"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RedirectShortURL(APIView):
    permission_classes = []
    def get(self, request, short_code, *args, **kwargs):
        short_url = get_object_or_404(ShortenedURL, short_code=short_code)
        return HttpResponseRedirect(short_url.original_url)

class AdGalleryList(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        ads = AdGallery.objects.filter(active=True)
        ad_list = []
        for ad in ads:
            ad_list.append({
                'title': ad.title,
                'description': ad.description,
                'image': ad.url,
                'type': ad.type
            })
        return Response(ad_list)