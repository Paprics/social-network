from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]


def validate_file_extension(value):
    ext = value.name.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Unsupported file extension: {ext}. Allowed: {ALLOWED_EXTENSIONS}")


def validate_file_size(value):
    limit_mb = 5
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"File too large. Size should not exceed {limit_mb} MB.")
