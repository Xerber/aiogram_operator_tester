import json
import sqlite3



with open('questions.json', encoding="utf8") as f:
    data = json.loads(f.read())


connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

categories = [{'category':'иптв', 'cat_id':1},
                 {'category':'общие', 'cat_id':2}, 
                 {'category':'подключение', 'cat_id':3}, 
                 {'category':'проблема', 'cat_id':4}, 
                 {'category':'финансы', 'cat_id':5}]
a = 1
for d in data:
  for cat in categories:
    if d['category'] == cat['category']:
      category_id = cat['cat_id']

  if d['level'] == 1:
    diff_level = 'easy'
  elif d['level'] == 2:
    diff_level = 'medium'
  elif d['level'] == 3:
    diff_level = 'hard'

  cursor.execute(f"INSERT INTO app_question VALUES ({a}, \'{diff_level}\', \'{d['text']}\', {category_id})")
  connection.commit()
  a+=1
