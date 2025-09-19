import shutil

from fastapi import UploadFile

from src.services.base import BaseService
from src.tasks.celery_tasks import resize_and_save_images


class ImageService(BaseService):
    def upload_image(self, file: UploadFile):
        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as f:
            shutil.copyfileobj(file.file, f)
        resize_and_save_images.delay(image_path)
