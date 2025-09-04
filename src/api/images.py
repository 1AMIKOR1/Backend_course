import  shutil

from fastapi import APIRouter, UploadFile

from src.tasks.celery_tasks import resize_and_save_images

router = APIRouter(prefix="/images", tags=["Работа с изображениями"])

@router.post("")
def upload_image(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as f:
        shutil.copyfileobj(file.file, f)

    resize_and_save_images.delay(image_path)