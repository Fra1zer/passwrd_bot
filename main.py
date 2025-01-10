from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from config import TOKEN


bot = Bot(token = TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_message(message: types.Message):
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Привет, это бот для создания паролей, напишу команду /help, чтобы узнать '
                                  'о возможностях бота.\n'
                                  'Если нужно связать с разработчиком, можешь написать ему - @fra1zer0')

@dp.message(Command('help'))
async def help_message(message: types.Message):
    await bot.send_message(chat_id= message.chat.id,
                           text = 'Доступные команды бота:')

@dp.message()
async def any_message(message: types.Message):
    await message.reply(text='Чтобы узнать возможности бота напишите команду - /help')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
