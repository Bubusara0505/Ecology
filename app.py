from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder='pages', static_folder='assets')

@app.route('/')
def index():
    cards = []
    if os.path.exists('data.txt'):
        with open('data.txt', 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 2:  # Проверяем, что есть и заголовок, и описание
                    title, description = parts
                    cards.append({'title': title, 'description': description})
    return render_template('index.html', cards=cards)

@app.route('/add_card', methods=['POST'])
def add_card():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if title and description:  # Проверяем, что поля не пустые
        with open('data.txt', 'a') as file:
            file.write(f"{title}|{description}\n")

    return redirect(url_for('index'))

@app.route('/records')
def records():
    cards = []
    if os.path.exists('data.txt'):
        with open('data.txt', 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    title, description = parts
                    cards.append({'title': title, 'description': description})
    return render_template('records.html', cards=cards)

if __name__ == '__main__':
    app.run(debug=True)