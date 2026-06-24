import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

from data.BOT_TOKEN import TOKEN


# TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set")


# GLOBAL PARAMETERS
cladding_section = 307
cladding_gap = 15

bot = Bot(TOKEN)
dp = Dispatcher()


async def calculate_positions(panel_width: int, amount_of_cladding: int) -> str:
    half = panel_width / 2 - cladding_gap / 2
    first_position = half - ((amount_of_cladding / 2) - 1) * cladding_section

    lines = []

    lines.append(f"first piece from cladding to plenum: ({int(first_position)})")

    for i in range(amount_of_cladding - 1):
        value = int(panel_width - (first_position + cladding_section * i))
        lines.append(str(value))

    lines.append(f"last piece from plenum to cladding: ({int(first_position)})")

    return "\n".join(lines)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Hi. Please enter the panel width and the number of claddings.\n\n"
        "Example:\n"
        "1452 5"
    )

# TODO #1
#   make multithreading for the calculation function
@dp.message()
async def calc(message: Message):
    try:
        panel_width, amount_of_cladding = map(int, message.text.split())

        result = await calculate_positions(panel_width, amount_of_cladding)

        await message.answer(result)

    except Exception:
        await message.answer(
            "Invalid format.\n\n"
            "Please enter the values as:\n"
            "1452 5"
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())