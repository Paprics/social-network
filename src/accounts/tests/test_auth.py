import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import UserProfileModel

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

@pytest.mark.django_db
class TestCustomUserModel:
    """
    Тестирует модель пользователя:
    - создание пользователя
    - автоматическое создание профиля
    - уникальность username, email и номера телефона
    - обработку отсутствующих обязательных полей
    """

    def test_create_user_and_profile(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            phone_number="+380931234567",
            password="password123"
        )
        assert user.pk is not None
        profile = UserProfileModel.objects.get(user=user)
        assert profile.user == user

    def test_unique_username(self):
        User = get_user_model()
        User.objects.create_user(username="uniqueuser", email="a@example.com", phone_number="+380931234568", password="pass123")
        with pytest.raises(IntegrityError):
            User.objects.create_user(username="uniqueuser", email="b@example.com", phone_number="+380931234569", password="pass123")

    def test_unique_email(self):
        User = get_user_model()
        User.objects.create_user(username="user1", email="unique@example.com", phone_number="+380931234570", password="pass123")
        with pytest.raises(IntegrityError):
            User.objects.create_user(username="user2", email="unique@example.com", phone_number="+380931234571", password="pass123")

    def test_unique_phone_number(self):
        User = get_user_model()
        User.objects.create_user(username="user3", email="c@example.com", phone_number="+380931234572", password="pass123")
        with pytest.raises(IntegrityError):
            User.objects.create_user(username="user4", email="d@example.com", phone_number="+380931234572", password="pass123")

    def test_create_user_without_username(self):
        User = get_user_model()
        with pytest.raises(ValueError):
            User.objects.create_user(
                username=None,
                email="test@example.com",
                phone_number="+380931234567",
                password="password123"
            )

    def test_create_user_without_email(self):
        User = get_user_model()
        # если email обязателен в модели и менеджере
        with pytest.raises(ValueError):
            User.objects.create_user(
                username="testuser",
                email=None,
                phone_number="+380931234567",
                password="password123"
            )

    def test_create_user_without_phone_number(self):
        User = get_user_model()
        with pytest.raises(ValueError):
            User.objects.create_user(
                username="testuser",
                email="test@example.com",
                phone_number=None,
                password="password123"
            )








    # def test_successful_registration(self, client):
    #     url = reverse('register')  # или твой урл регистрации
    #     data = {
    #         'username': 'testuser',
    #         'phone_number': '+380931234567',
    #         'email': 'test@example.com',
    #         'password1': 'StrongPass123!',
    #         'password2': 'StrongPass123!',
    #     }
    #
    #     response = client.post(url, data)
    #     assert response.status_code == 302 or 201  # зависит от реализации
    #
    #     User = get_user_model()
    #     user = User.objects.filter(username='testuser').first()
    #     assert user is not None
    #     assert user.email == 'test@example.com'
    #     assert user.phone_number == '+380931234567'

    def test_registration_with_invalid_phone(self):
        pass

class TestLogin:
    def test_login_successful(self):
        pass

    def test_login_wrong_password(self):
        pass
