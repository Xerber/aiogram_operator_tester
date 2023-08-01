import aiosqlite
import pathlib
from pathlib import Path


db_path = Path(pathlib.Path.cwd().parent,'db.sqlite3')


async def get_difficult():
  async with aiosqlite.connect(db_path) as db:
    async with db.execute('SELECT * FROM app_test_levels') as cursor:
      levels = await cursor.fetchall()
      return(levels)


async def get_test_question_qty(title_id):
  async with aiosqlite.connect(db_path) as db:
    async with db.execute(f'SELECT * FROM app_test_question_qty WHERE title_id={title_id}') as cursor:
      question_qty = await cursor.fetchall()
      return(question_qty)


async def get_questions(category_id,diff_level):
  async with aiosqlite.connect(db_path) as db:
    async with db.execute(f'SELECT * FROM app_question WHERE category_id={category_id} and diff_level=\"{diff_level}\"') as cursor:
      questions = await cursor.fetchall()
      return(questions)
