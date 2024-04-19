# Импортируем необходимые модули
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Функция для создания таблицы в базе данных, если она еще не существует
def create_table():
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS words
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, definition TEXT)''')
    conn.commit()
    conn.close()

# Функция для поиска слова в базе данных
def search_word(word):
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute("SELECT * FROM words WHERE word=?", (word,))
    result = c.fetchone()
    conn.close()
    return result

# Определяем маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Определяем маршрут для страницы добавления слов
@app.route('/add_word', methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        word = request.form['word']
        definition = request.form['definition']
        conn = sqlite3.connect('dictionary.db')
        c = conn.cursor()
        c.execute("INSERT INTO words (word, definition) VALUES (?, ?)", (word, definition))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_word.html')

# Определяем маршрут для поиска слова
@app.route('/search_word', methods=['POST'])
def search():
    word = request.form['search_word']
    result = search_word(word)
    if result:
        return render_template('word.html', word=result[1], definition=result[2])
    else:
        return render_template('word.html', word="Word not found", definition="")

# Запускаем функцию для создания таблицы при запуске приложения
create_table()

if __name__ == '__main__':
    app.run(debug=True)
