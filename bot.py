import logging
import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.client.bot import DefaultBotProperties

from data.BOT_TOKEN import TOKEN

# TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set")

# GLOBAL PARAMETERS

cladding_section = 308.66
# cladding_section = 307
# cladding_gap = 15
cladding_gap = 16

bot = Bot(TOKEN)
dp = Dispatcher()


async def calculate_positions(panel_width: int, amount_of_cladding: int) -> str:
    half = panel_width / 2 - cladding_gap / 2
    first_position = half - ((amount_of_cladding / 2) - 1) * cladding_section

    lines = []

    lines.append(f"Gap: {cladding_gap} mm\n Cladding Section: {cladding_section} mm")

    lines.append(f"First piece from cladding to plenum: ({int(first_position)})")

    for i in range(amount_of_cladding - 1):
        value = int(panel_width - (first_position + cladding_section * i))
        lines.append(str(value))

    lines.append(f"last piece from plenum to cladding: ({int(first_position)})")

    return "\n".join(lines)

# async def start():
#     logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s) .%(funcName)s(%(lineno)d) - %(message)s")
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

#     dp = Dispatcher()
#     await handlers_reg(dp)


# async def handlers_reg(dp: Dispatcher):

#     # command handler registration 
#     dp.message.register(get_start, Command(commands=['start']))
#     dp.message.register(get_feedback, Command(commands=['feedback']))
#     dp.message.register(settings, Command(commands=['settings']))
#     dp.message.register(get_version, Command(commands=['version']))

#     # FEEDBACK 
#     dp.message.register(feedback_from_user, FeedbackForm.RECEIVING_FEEDBACK)

#     # TEXT HANDLER
#     dp.message.register(text_handler, F.text)

#     # DOCUMENTS HANDLER
#     dp.message.register(document_handler, F.document)

#     # AFTER START BOT COMMANDS
#     dp.startup.register(start_bot)
#     dp.shutdown.register(stop_bot)    


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Hi. Please enter the panel width and the number of claddings.\n\n"
        "Example:\n"
        "1452 5"
    )

# async def start_bot(bot: Bot):
#     await set_commands(bot)
#     try:
#         await start_db()
#     except Exception as e:    
#         print('[err 8989898]', e)
#     try:
#         for admin_id in ADMINS_ID:
#             await bot.send_message(admin_id, "<b>BOT STARTED</b>")
#     except Exception as e:
#         print('[-][ERROR SEND MESSAGE TO ADMIN]', e)


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