from django.conf import settings
from django.db import models
from django.utils.text import slugify

from mediafiles.utils import user_avatar_upload_path

from .validators import validate_file_extension, validate_file_size


class AlbumModel(models.Model):
    PRIVACY_CHOICES = [
        ("private", "Private (owner only)"),
        ("friends", "Friends only"),
        ("public", "Public (everyone)"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="albums")
    title = models.CharField(blank=False, max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.CharField(blank=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default="public")
    is_active = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title or "profile-photos")
            slug = base_slug
            counter = 1
            while AlbumModel.objects.filter(owner=self.owner, slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def can_view(self, user):
        if not self.is_active:
            return False

        if self.privacy == "public":
            return True

        if not user.is_authenticated:
            return False

        if self.owner == user:
            return True

        if self.privacy == "friends":
            return hasattr(self.owner, "friends") and user in self.owner.friends.all()

        return False

    def __str__(self):
        return f"{self.title} by {self.owner.username} ({self.privacy})"

    class Meta:
        db_table = "albums"
        ordering = ["-created_at"]


class PhotoModel(models.Model):
    CONTEXT_CHOICES = [
        ("avatar", "Profile photo"),
        ("dialog", "Dialog Image"),
        ("chat", "Public Chat"),
        ("album", "Album Photo"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="photos")
    album = models.ForeignKey("AlbumModel", on_delete=models.CASCADE, null=False, blank=False, related_name="photos")
    image = models.ImageField(
        upload_to=user_avatar_upload_path,
        validators=[validate_file_extension, validate_file_size],
    )
    description = models.CharField(blank=True, max_length=250)

    context = models.CharField(max_length=10, choices=CONTEXT_CHOICES, default="album")

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def can_view(self, user):
        # Проксируем проверку доступа через альбом
        return self.album.can_view(user)

    def __str__(self):
        return f"Photo {self.id} by {self.owner.username} ({self.context})"

    class Meta:
        db_table = "photos"
