from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from config import TOKEN
from generate_passwrd import generate_password

bot = Bot(token = TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Password(StatesGroup):
    gen_passwrd = State()


@dp.message(Command('start'), StateFilter(default_state))
async def start_message(message: types.Message) -> None:
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Привет, это бот для создания паролей, напишу команду /help, чтобы узнать '
                                  'о возможностях бота.\n'
                                  'Если нужно связать с разработчиком, можешь написать ему - @fra1zer0')


@dp.message(Command('help'), StateFilter(default_state))
async def help_message(message: types.Message) -> None:
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Доступные команды бота: /generate')


@dp.message(Command('generate'), StateFilter(default_state))
async def generate_message(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Password.gen_passwrd)
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Напишите длину пароля: ')


@dp.message(StateFilter(Password.gen_passwrd))
async def process_gen(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    password = generate_password(int(message.text))
    await bot.send_message(chat_id = message.chat.id,
                           text = f'Сгенерированный пароль: {password}')
    await state.clear()


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
