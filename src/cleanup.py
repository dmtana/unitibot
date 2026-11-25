import os
import time
import asyncio
import logging


async def cleanup_photos(
    folder,
    max_age=3600,
    interval=300
):
    while True:
        try:
            if os.path.isdir(folder):

                current_time = time.time()

                for filename in os.listdir(folder):

                    file_path = os.path.join(folder, filename)

                    if not os.path.isfile(file_path):
                        continue

                    if not filename.lower().endswith(
                        (".jpg", ".jpeg", ".png", ".webp")
                    ):
                        continue

                    try:
                        file_age = current_time - os.path.getmtime(
                            file_path
                        )

                        if file_age > max_age:
                            os.remove(file_path)

                            logging.info(
                                f"Deleted expired photo: {filename}"
                            )

                    except OSError as e:
                        logging.error(f"Cleanup error: {e}")

        except Exception:
            logging.exception("Photo cleanup failed")

        await asyncio.sleep(interval)