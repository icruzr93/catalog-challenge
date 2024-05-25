from unittest.mock import patch

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app.catalog.models import Brand, Product
from app.core.models import User


class BrandTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.group = Group.objects.create(name="tests")
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpass",
            groups=self.group,
        )
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

    def test_create_brand(self):
        url = reverse("brands")
        data = {"name": "Test Brand"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_brands(self):
        url = reverse("brands")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_brand_detail(self):
        brand = Brand.objects.create(name="Test Brand")
        url = reverse("brand-detail", kwargs={"pk": brand.pk})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_brand(self):
        brand = Brand.objects.create(name="Test Brand")
        url = reverse("brand-detail", kwargs={"pk": brand.pk})
        data = {"name": "Updated Brand"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_brand(self):
        brand = Brand.objects.create(name="Test Brand")
        url = reverse("brand-detail", kwargs={"pk": brand.pk})
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        self.brand = Brand.objects.create(name="Test Brand")

    @patch("app.catalog.tasks.on_product_created.delay", return_value=None)
    def test_create_product(self, mock_on_product_created):
        url = reverse("products")
        data = {"name": "Test Product", "sku": "123123123", "brand_id": self.brand.id}
        response = self.client.post(url, data, format="json")

        # Assert function was called once
        mock_on_product_created.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_products(self):
        url = reverse("products")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_detail(self):
        product = Product.objects.create(name="Test Product", brand=self.brand)
        url = reverse("product-detail", kwargs={"pk": product.pk})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.catalog.tasks.on_product_updated.delay", return_value=None)
    def test_update_product(self, mock_on_product_updated):
        product = Product.objects.create(name="Test Product", brand=self.brand)
        url = reverse("product-detail", kwargs={"pk": product.pk})
        data = {"name": "Updated Product"}
        response = self.client.patch(url, data, format="json")

        # Assert function was called once
        mock_on_product_updated.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.catalog.tasks.on_product_deleted.delay", return_value=None)
    def test_delete_product(self, mock_on_product_deleted):
        product = Product.objects.create(name="Test Product", brand=self.brand)
        url = reverse("product-detail", kwargs={"pk": product.pk})
        response = self.client.delete(url, format="json")

        # Assert function was called once
        mock_on_product_deleted.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
