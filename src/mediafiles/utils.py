import os
import shortuuid

def user_avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]  # расширение, например '.jpg'
    new_filename = f"{shortuuid.uuid()}{ext}"
    return f"users/{instance.owner.uuid}/avatars/{new_filename}"