from rest_framework import status
from rest_framework.test import APITestCase

from main.models import NetworkLink, Product
from users.models import User
from django.urls import reverse


class TestApi(APITestCase):
    """
    Тестирование механизмов CRUD и других контроллеров, прав доступа

    """

    def setUp(self):
        self.user = User.objects.create(email='test@test.com',
                                        password="1234",
                                        first_name='Test',
                                        last_name='Testov')
        self.user.save()
        self.user_super_admin = User.objects.create(email='test_super@test.com',
                                                    password=12345,
                                                    first_name='Test',
                                                    last_name='Testov',
                                                    is_superuser=True
                                                    )
        self.user_super_admin.save()
        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(
            title="Test product",
            launch_date="2024-05-03",
            author=self.user
        )
        self.product.save()

        self.network_link = NetworkLink.objects.create(
            title="Test1",
            network_level=0,
            email="test1@mail.ru",
            country="Russia",
            city="Moscow",
            street="Lenina",
            house_number=1,
            author=self.user
        )
        self.network_link.product.add(self.product)
        self.network_link.save()

    def test_create_product(self):
        """Тест для создания товара"""
        url = reverse('main:product-list')
        data = {
            'title': "Test product",
            'launch_date': "2024-05-03"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_list_products(self):
        """Получение списка товаров"""
        url = reverse('main:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(Product.objects.count(), 1)

    def test_detail_product(self):
        """Подробнее о товаре"""
        url = reverse('main:product-detail', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        """Обновлениe товара"""
        url = reverse('main:product-detail', kwargs={'pk': self.product.pk})
        data = {'title': "Change product",
                'launch_date': "2024-05-04"}
        response = self.client.put(url, data, author=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Change product')

    def test_delete_product(self):
        """Удаление товара"""
        url = reverse('main:product-detail', kwargs={'pk': self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_network_link(self):
        """Тест для создания звена сети"""
        url = reverse('main:network-link-create')
        data = {
            "title": "Test",
            "network_level": 0,
            "email": "test@mail.ru",
            "country": "Russia",
            "city": "Moscow",
            "street": "Lenina",
            "house_number": 5,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkLink.objects.count(), 2)

    def test_create_network_link_not_right(self):
        """Тест для создания объявления с неверными данными"""
        url = reverse('main:network-link-create')
        data_error = {
            "title": "Test",
            "network_level": 0,
            "email": "test@mail.ru",
            "country": "Russia",
            "city": "Moscow",
            "street": "Lenina",
            "house_number": 5,
            "debt_to_supplier": 1200568.68
        }
        response = self.client.post(url, data_error, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_network_link_not_authenticated(self):
        """Тест для создания объявления без аутентификации"""
        url = reverse('main:network-link-create')
        data = {
            "title": "Test",
            "network_level": 0,
            "email": "test@mail.ru",
            "country": "Russia",
            "city": "Moscow",
            "street": "Lenina",
            "house_number": 5
        }
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_network_links(self):
        """Получение списка звеньев сети"""
        url = reverse('main:network-links-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(NetworkLink.objects.count(), 1)

    def test_list_my_network_link(self):
        """Список моих звеньев сети"""
        url = reverse('main:my-network-link-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_network_link(self):
        """Информации об звене сети"""
        url = reverse('main:network-link-detail', kwargs={'pk': self.network_link.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test1')

    def test_update_network_link(self):
        """Обновлениe звена сети"""
        url = reverse('main:network-link-update', kwargs={'pk': self.network_link.pk})
        data = {'title': 'Change test',
                'country': 'USA'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['country'], 'USA')

    def test_delete_network_link(self):
        """Удаление звена сети"""
        url = reverse('main:network-link-delete', kwargs={'pk': self.network_link.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NetworkLink.objects.count(), 0)

    def test_retrieve_product_with_network_links(self):
        """Информации об звене сети"""
        url = reverse('main:product-detail-network-links', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['network_links'][0]['title'], 'Test1')

    def test_access_admin_is_not_active(self):
        """
        Тест для проверки прав доступа к API
        """

        self.user.is_active = False
        self.user.save()
        url = reverse('main:network-link-delete', kwargs={'pk': self.network_link.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'detail': 'У вас нет прав активного админа!'})

    def test_set_admin_is_not_active(self):
        """
        Тест для включения/выключения активности админов
        """

        self.client.force_authenticate(user=self.user_super_admin)
        url = reverse('users:set_active_adnin', kwargs={'pk': self.user.id})
        response = self.client.post(url)
        self.user.save()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Админ Testov не имеет больше доступ к API!'})
