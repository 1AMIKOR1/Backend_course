from fastapi import APIRouter, UploadFile

from src.services.images import ImageService

router = APIRouter(prefix="/images", tags=["Работа с изображениями"])


@router.post("/",summary="Добавление изображений")
def upload_image(file: UploadFile):
    ImageService().upload_image(file)
