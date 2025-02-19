import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from database import *
from generate_passwrd import generate_password, generate_pincode


bot = Bot(token = TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
logging.basicConfig(level=logging.INFO, filename="logs_bot.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")


class Password(StatesGroup):
    gen_passwrd = State()


class Pin(StatesGroup):
    gen_pin = State()


@dp.message(Command('start'), StateFilter(default_state))
async def start_message(message: types.Message) -> None:
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Привет, это бот для создания паролей, напишите команду /help, чтобы узнать '
                                  'о возможностях бота.\n'
                                  'Если нужно связать с разработчиком, можете написать ему - @fra1zer0')
    user_id = message.from_user.id
    add_user(user_id)
    logging.info(f'Пользователь {user_id} начал работу с ботом')


@dp.message(Command('help'), StateFilter(default_state))
async def help_message(message: types.Message) -> None:
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Доступные команды бота:\n'
                                  '/gen_pass - генерация пароля\n'
                                  '/gen_pin - генерация пин-кода\n'
                                  '/get_count - количество сгенерированных паролей/пинкодов')
    logging.info(f'Пользователь {message.from_user.id} вызвал /help')


@dp.message(Command('gen_pass'), StateFilter(default_state))
async def generate_message(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Password.gen_passwrd)
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Напишите длину пароля(от 8 до 120 символов)')
    logging.info(f'Пользователь {message.user_id} начал генерацию пароля')


@dp.message(StateFilter(Password.gen_passwrd), lambda x: x.text.isdigit() and 8 <= int(x.text) <= 120)
async def process_gen_pass(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(gen_passwrd=message.text)

    try:
        password = generate_password(int(message.text))
        await bot.send_message(chat_id=message.chat.id, text=f'Сгенерированный пароль: {password}')
        logging.info(f'Пароль {password} успешно сгенерирован для пользователя {user_id}.')

        update_count(user_id)
    except Exception as err:
        logging.error(f'Ошибка при генерации пароля для пользователя {user_id}: {err}')
    finally:
        await state.clear()
        logging.info(f'Состояние для пользователя {user_id} очищено.')


@dp.message(StateFilter(Password.gen_passwrd))
async def warning_pass(message: types.Message):
    await message.answer(text='Введите число от 8 до 120\n'
                              'Попробуйте ещё раз')


@dp.message(Command('gen_pin'), StateFilter(default_state))
async def generate_pin(message: types.Message, state: FSMContext):
    await state.set_state(Pin.gen_pin)
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Напишите длину пин-кода(от 4 до 16 символов)')
    logging.info(f'Пользователь {message.user_id} начал генерацию пинкода')


@dp.message(StateFilter(Pin.gen_pin), lambda x: x.text.isdigit() and 4 <= int(x.text) <= 16)
async def process_gen_pin(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(gen_pin=message.text)

    try:
        pin = generate_pincode(int(message.text))
        await bot.send_message(chat_id=message.chat.id, text=f'Сгенерированный пин-код: {pin}')
        logging.info(f'Пин-код {pin} успешно сгенерирован для пользователя {user_id}.')
        update_count(user_id)
    except Exception as err:
        logging.error(f'Ошибка при генерации пин-кода для пользователя {user_id}: {err}')
    finally:
        await state.clear()
        logging.info(f'Состояние для пользователя {user_id} очищено.')


@dp.message(StateFilter(Pin.gen_pin))
async def warning_pin(message: types.Message):
    await message.answer(text = 'Введите число от 4 до 16\n'
                                'Попробуйте ещё раз')


@dp.message(Command('get_count'))
async def take_count(message: types.Message):
    user_id = message.from_user.id
    count = get_count(user_id)
    await bot.send_message(chat_id=message.chat.id,
                           text = f'Количество сгенерированных паролей/пин-кодов: {count}')
    logging.info(f'Пользователь {user_id} вызвал /get_count')


@dp.message()
async def any_message(message: types.Message):
    await message.reply(text = 'Чтобы посмотреть доступные команды напишите /help')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    create_table()
    asyncio.run(main())
