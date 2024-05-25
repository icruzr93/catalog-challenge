from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Brand, Product
from .serializers import BrandSerializer, ProductSerializer
from .tasks import on_product_created, on_product_deleted, on_product_updated


class ProductListCreateView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]

        return [AllowAny()]

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            brand_id = self.request.data.get("brand_id")
            instance = serializer.save(brand_id=brand_id)
            user = self.request.user

            on_product_created.delay(instance.pk, user.pk)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]

        return [AllowAny()]

    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(instance)

        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    def patch(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Product, pk=pk)

        if instance.deleted:
            return Response(
                {"detail": "Object does not exists"}, status=status.HTTP_404_NOT_FOUND
            )

        user = self.request.user
        on_product_updated.delay(instance.pk, user.pk)

        serializer = ProductSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Product, pk=pk)

        if instance.deleted:
            return Response(
                {"message": "Object does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = self.request.user
        on_product_deleted.delay(instance.pk, user.pk)
        instance.deleted = datetime.now()
        instance.save()

        return Response(
            {"message": "Object deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class BrandListCreateView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]

        return [AllowAny()]

    def get(self, request, *args, **kwargs):
        queryset = Brand.objects.all()
        serializer = BrandSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BrandSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandDetailView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]

        return [AllowAny()]

    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Brand, pk=pk)
        serializer = BrandSerializer(instance)

        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    def patch(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Brand, pk=pk)

        if instance.deleted:
            return Response(
                {"detail": "Object does not exists"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BrandSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Brand, pk=pk)
        serializer = BrandSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Brand, pk=pk)
        if instance.deleted:
            return Response(
                {"message": "Object does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )

        instance.deleted = datetime.now()
        instance.save()

        return Response(
            {"message": "Object deleted"}, status=status.HTTP_204_NO_CONTENT
        )
