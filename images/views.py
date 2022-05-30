from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework.parsers import JSONParser

from drf_spectacular.utils import extend_schema, inline_serializer

from .apps import scheduler
from .models import Image
from .serializers import ImageSerializer, ImageCreationSerializer
from .extractor import Extractor

class ListImage(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @extend_schema(
        request=ImageCreationSerializer,
        responses={201: ImageCreationSerializer},
        description="Provide image URL to be analyzed. Response is url where information about the image can be found (because image analysis is done in the background)."
    )
    def post(self, request, *args, **kwargs):
        serializer = ImageCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        extractor = Extractor(serializer.validated_data["url"])
        if (extractor.verify()):
            # URL is valid and is image, first create new entry in db
            image = Image(url=serializer.validated_data["url"])
            image.save()
            # Get url for newly created entry
            obj_url = reverse('image-detail', args=[image.pk], request=request)
            headers = {'Location': obj_url}
            # Schedule processing of the image
            scheduler.add_job(extractor.extractAndSave, args=[image.pk])
            return Response({"url": obj_url}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "URL is not a valid image"}, status=status.HTTP_400_BAD_REQUEST)
        

class DetailImage(generics.RetrieveDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer