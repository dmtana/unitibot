import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message

from aiogram import Bot, F, Router
from aiogram.types import Message, FSInputFile

from src.bellara_scanner import scan
from src.bellara_calc import calc_

router = Router()



from data.BOT_TOKEN import TOKEN

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set")

# GLOBAL PARAMETERS

# WAHA_CONFIG
cladding_section = 306.33
cladding_gap = 14

# WAHA_LTC_CONFIG_FOR_BELLARA_LIGHT
adjustment      = 0.33
panel_width     = 0
gap_last_piece  = 4
S = 93  -adjustment
M = 135 -adjustment
L = 199 -adjustment
first_piece = 157
# sample_line     = 'MSMLMMSLMLLSMLMLSML'
c = 0


dp = Dispatcher()
router = Router()


async def calculate_positions(panel_width: int, amount_of_cladding: int) -> str:
    half = panel_width / 2 - cladding_gap / 2
    first_position = half - ((amount_of_cladding / 2) - 1) * cladding_section

    lines = [
        f"<b>Gap: {cladding_gap} mm\nCladding Section: {cladding_section} mm\n</b>",
        "It works only for symmetrical cladding! ",
        f"First and last piece cut length: <b>{round(first_position - 12)}</b>",
        f"First piece from cladding to plenum: <b>({int(first_position)})</b>",
        f"From cladding to Joggle Cleat (JOG): <b>({int(first_position - 73)})</b>",
    ]

    for i in range(amount_of_cladding - 1):
        value = round(panel_width - (first_position + cladding_section * i))
        lines.append(str(value))

    return "\n".join(lines)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Hi. Please enter the panel width and the number of claddings.\n\n"
        "Example:\n"
        "1452 5"
    )


@router.message(F.text)
async def calc(message: Message):
    try:
        panel_width, amount_of_cladding = map(int, message.text.split())
        result = await calculate_positions(panel_width, amount_of_cladding)
        await message.answer(result)
    except ValueError:
        await message.answer(
            "Invalid format.\n\n"
            "Please enter the values as:\n"
            "1452 5"
        )



@router.message(F.photo)
async def photo_handler(message: Message, bot: Bot):

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    current_path = os.path.dirname(__file__)
    photo_dir = os.path.join(current_path, "photos")

    os.makedirs(photo_dir, exist_ok=True)

    filename = f"{photo.file_unique_id}.jpg"
    file_path = os.path.join(photo_dir, filename)

    msg_caption = None

    try:
        # Download photo
        await bot.download_file(file.file_path, file_path)

        status = await message.answer("Processing image...")

        # Run scanner without blocking the bot
        result = await asyncio.to_thread(
            scan,
            file_path,
            first="L"
        )

        sequence = result["sequence"]
        counts = result["counts"]

        measurments = ''

        if message.caption:
            try:
                measurments+='\n\nMeasurments: \n'+calc_(sequence, message.caption)
            except Exception:
                await message.answer("ERR MSG, try againg...")
        
        # Send processed image
        await message.answer_photo(
            photo=FSInputFile(result["output"]),
            caption=(
                f"Sequence: {sequence}\n\n"
                f"Small: {counts.get('S', 0)}\n"
                f"Medium: {counts.get('M', 0)}\n"
                f"Large: {counts.get('L', 0)}\n\n"
                f"Total: {len(sequence)}"
                f"{measurments}"
        
            )
        )

        await status.delete()

    except Exception:
        logging.exception("Photo processing failed")
        await message.answer("Failed to process image.")



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s) .%(funcName)s(%(lineno)d) - %(message)s",
    )
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except Exception as ex:
        print(f"[ERROR IN START FILE] {ex}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())