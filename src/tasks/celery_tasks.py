import asyncio
import logging
import os
from time import sleep

from PIL import Image

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print("Test task done")


@celery_instance.task
def resize_and_save_images(
    input_image_path: str,
    output_dir: str = "src/static/images",
    widths: list | None = None,
):
    logging.debug(f"Вызывается функция с {input_image_path=}")
    os.makedirs(output_dir, exist_ok=True)
    if not widths:
        widths = [1000, 500, 200]

    with Image.open(input_image_path) as img:
        original_width, original_height = img.size

        for width in widths:
            # Вычисляем высоту, сохраняя пропорции
            ratio = width / original_width
            new_height = int(original_height * ratio)

            # Изменяем размер
            resized_img = img.resize(
                (width, new_height), Image.Resampling.LANCZOS
            )

            # Получаем имя файла без пути и расширение
            base_name = os.path.basename(input_image_path)
            file_name, ext = os.path.splitext(base_name)

            # Формируем новое имя файла
            new_file_name = f"{file_name}_{width}px{ext}"
            output_path = os.path.join(output_dir, new_file_name)

            # Сохраняем изображение
            resized_img.save(output_path)
            logging.info(
                f"Изображение сохранено в размерах:{widths} в папку:{output_path}"
            )


async def get_bookings_with_today_chekin_helper():
    logging.debug("START")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        logging.debug(f"{bookings=}")


@celery_instance.task(name="booking_today_chekin")
def send_emails_to_user_with_today_checkin():
    asyncio.run(get_bookings_with_today_chekin_helper())
