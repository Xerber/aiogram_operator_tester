from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import os
import random
from dotenv import load_dotenv, find_dotenv
from dbwork import *


load_dotenv(find_dotenv())

storage = MemoryStorage()
bot = Bot(os.getenv('TOKEN_API'))
dp = Dispatcher(bot,storage=storage)

class StartTestGroup(StatesGroup):
  name = State()
  diff_level = State()
  checking = State()
  in_progress = State()

@dp.message_handler(commands=['cancel'], state="*")
async def cancel_command(message: types.Message, state: FSMContext):
  current_state = await state.get_state()
  if current_state is None:
    return
  await state.finish()
  await message.answer('Состояние было сброшено')

@dp.message_handler(commands=['ok'], state=StartTestGroup.checking)
async def ok_command(message: types.Message, state: FSMContext):
  current_state = await state.get_state()
  diff_levels = ('easy', 'medium', 'hard')
  questions_pool = []
  async with state.proxy() as data:
    config = await get_test_question_qty((data['level'].split('.'))[0])
    for row in config:
      i = 0
      for qty in row[1:4]:
        if qty>0:
          questions = await get_questions(row[4],diff_levels[i])
          random.shuffle(questions)
          for question in questions[0:qty]:
            questions_pool.append({'question':question})
            i+=1
    data['questions'] = questions_pool
  await message.answer(f'''Всего собралось {len(questions_pool)} вопросов. Готовы?
/go - для начала теста
или
/cancel - для отмены''')

@dp.message_handler(commands=['go'],state=StartTestGroup.checking)
async def go_command(message: types.Message, state: FSMContext):
  current_state = await state.get_state()
  await StartTestGroup.in_progress.set()
  async with state.proxy() as data:
    data['question'] = 1
    await message.answer(f'''Вопрос {data["question"]}/{len(data["questions"])}
id: {data["questions"][data['question']-1]["question"][0]}
сложность: {data["questions"][data['question']-1]["question"][1]}
Вопрос:{data["questions"][data['question']-1]["question"][2]}''')
    data['question'] += 1

@dp.message_handler(commands=['test'], state=None)
async def test_command(message: types.Message):
  await StartTestGroup.name.set()
  await message.answer(text='''Введи имя/ник опрашиваемого 
или 
/cancel - для отмены''')

@dp.message_handler(state=StartTestGroup.name)
async def add_diff_level(message: types.Message, state: FSMContext):
  await StartTestGroup.diff_level.set()
  async with state.proxy() as data:
    data['name'] = message.text
  levels = await get_difficult()
  kb = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
  for level in levels:
    kb.add(KeyboardButton(f'{level[0]}. {level[1]}'))
  await message.answer(f'''Будем опрашивать {data["name"]}. Теперь выбери тест
или 
/cancel - для отмены''', reply_markup=kb)

@dp.message_handler(state=StartTestGroup.diff_level)
async def checking_info(message: types.Message, state: FSMContext):
  await StartTestGroup.checking.set()
  async with state.proxy() as data:
    data['level'] = message.text
    await message.answer(f'''Будем опрашивать {data["name"]} по тесту {(data["level"].split('.'))[1]}. Выбери
/ok - если всё корректно
или 
/cancel - для отмены''')

@dp.message_handler(state=StartTestGroup.in_progress)
async def test_cycle(message: types.Message, state: FSMContext):
  current_state = await state.get_state()
  async with state.proxy() as data:
    print(data["questions"])
    if data['question'] > len(data["questions"]):
      data['questions'][data['question']-2] = {'question':data['questions'][data['question']-2]['question'][2],'grade':message.text}
      await state.finish()
      grade = 0
      for question in data['questions']:
        grade += int(question['grade'])
      oper_grade = round(100/len(data['questions'])*grade)
      await message.answer(f'''{data["name"]} завершил тест с оценкой: {oper_grade}''')
    else:
      data['questions'][data['question']-2] = {'question':data['questions'][data['question']-2]['question'][2],'grade':message.text}
      await message.answer(f'''Вопрос {data["question"]}/{len(data["questions"])}
id: {data["questions"][data['question']-1]["question"][0]}
сложность: {data["questions"][data['question']-1]["question"][1]}
Вопрос:{data["questions"][data['question']-1]["question"][2]}''')
      data['question'] += 1


if __name__=='__main__':
  executor.start_polling(dp, skip_updates=True)
