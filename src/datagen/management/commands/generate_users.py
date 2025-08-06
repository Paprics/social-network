from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

User = get_user_model()
faker = Faker()


class Command(BaseCommand):
    help = "Генерирует фейковых пользователей для тестов и наполнения базы"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10, help="Сколько пользователей создать (по умолчанию 10)")

    def handle(self, *args, **options):
        count = options["count"]

        for _ in range(count):
            username = faker.user_name()
            email = faker.email()
            phone_number = faker.phone_number()

            # Создаём юзера
            user = User.objects.create_user(  # noqa 841
                username=username,  # noqa 401
                email=email,
                phone_number=phone_number,
                password="test12345",  # дефолтный пароль для всех
            )

            # # Если у модели User есть доп. поля — заполняем
            # if hasattr(user, "profile"):  # например, у тебя может быть модель Profile
            #     user.profile.bio = faker.text(max_nb_chars=100)
            #     user.profile.save()

            self.stdout.write(self.style.SUCCESS(f"✅ Создан пользователь: {username}"))
