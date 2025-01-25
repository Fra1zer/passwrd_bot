from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from config import TOKEN
from generate_passwrd import generate_password, generate_pincode


bot = Bot(token = TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class Password(StatesGroup):
    gen_passwrd = State()


class Pin(StatesGroup):
    gen_pin = State()


@dp.message(Command('start'), StateFilter(default_state))
async def start_message(message: types.Message) -> None:
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Привет, это бот для создания паролей, напишу команду /help, чтобы узнать '
                                  'о возможностях бота.\n'
                                  'Если нужно связать с разработчиком, можешь написать ему - @fra1zer0')


@dp.message(Command('help'), StateFilter(default_state))
async def help_message(message: types.Message) -> None:
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Доступные команды бота: /gen_pass, /gen_pin')


@dp.message(Command('gen_pass'), StateFilter(default_state))
async def generate_message(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Password.gen_passwrd)
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Напишите длину пароля(от 8 до 120 символов)')


@dp.message(StateFilter(Password.gen_passwrd), lambda x: x.text.isdigit() and 8 <= int(x.text) <= 120)
async def process_gen_pass(message: types.Message, state: FSMContext):
    await state.update_data(gen_passwrd = message.text)
    password = generate_password(int(message.text))
    await bot.send_message(chat_id = message.chat.id,
                           text = f'Сгенерированный пароль: {password}')
    await state.clear()


@dp.message(StateFilter(Password.gen_passwrd))
async def warning_pass(message: types.Message):
    await message.answer(text='Введите число от 8 до 120\n'
                              'Попробуйте ещё раз')


@dp.message(Command('gen_pin'), StateFilter(default_state))
async def generate_pin(message: types.Message, state: FSMContext):
    await state.set_state(Pin.gen_pin)
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Напишите длину пинкода(от 4 до 16 символов)')


@dp.message(StateFilter(Pin.gen_pin), lambda x: x.text.isdigit() and 4 <= int(x.text) <= 16)
async def process_gen_pin(message: types.Message, state: FSMContext):
    await state.update_data(gen_pin = message.text)
    pin = generate_pincode(int(message.text))
    await bot.send_message(chat_id = message.chat.id,
                           text = f'Сгенерированный пинкод: {pin}')
    await state.clear()


@dp.message(StateFilter(Pin.gen_pin))
async def warning_pin(message: types.Message):
    await message.answer(text = 'Введите число от 4 до 16\n'
                                'Попробуйте ещё раз')


@dp.message()
async def any_message(message: types.Message):
    await message.reply(text = 'Чтобы посмотреть доступные команды напишите /help')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
