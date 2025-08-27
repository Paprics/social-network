import os

import shortuuid


def album_photo_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = f"{shortuuid.uuid()}{ext}"

    if getattr(instance, "context", None) == "avatar":
        return f"users/albums/{instance.owner.uuid}-{instance.owner.pk}/profile_photo/{new_filename}"

    # Обычные альбомы
    return f"users/albums/{instance.owner.uuid}-{instance.owner.pk}/{instance.album.slug}/{new_filename}"
