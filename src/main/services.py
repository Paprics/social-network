from django.contrib.auth import get_user_model
import faker

User = get_user_model()


def generate_new_user(quntity=10):
