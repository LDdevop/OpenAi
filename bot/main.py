import os
import dotenv
import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


dotenv.load_dotenv()
bot = Bot(os.getenv('TELEBOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    """States for user actions"""
    question = State()


@dp.message_handler(commands=['start', 'get_answer'])
async def commands_handler(message: types.Message):
    """Processing all commands"""
    if message.text == '/start':
        await message.answer(f'Hello, {message.from_user.first_name}')

    elif message.text == '/get_answer':
        await message.answer('Please enter your question: ')
        await Form.question.set()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """ Allow user to cancel any action """
    current_state = await state.get_state()
    if current_state is None:
        return await message.answer('Nothing to cancel')

    await state.finish()
    await message.answer('Cancelled.')


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.question)
async def process_question_invalid(message: types.Message):
    """If question is invalid"""
    return await message.answer('Please enter right question')


@dp.message_handler(state=Form.question)
async def process_question(message: types.Message, state: FSMContext):
    """Make a request by user's question"""
    await state.finish()
    question = message.text

    try:
        response = requests.get(f'http://127.0.0.1:8000/get_answer/{question}').json()
        await message.answer(response['message'])

    except requests.exceptions.ConnectionError:
        await message.answer('Sorry OpenAi not available')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
