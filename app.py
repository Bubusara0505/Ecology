from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json

app = Flask(__name__, template_folder='pages', static_folder='assets')

@app.route('/')
def index():
    cards = []
    if os.path.exists('data.txt'):
        with open('data.txt', 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    title, description = parts
                    cards.append({'title': title, 'description': description})
    return render_template('index.html', cards=cards)

@app.route('/add_card', methods=['POST'])
def add_card():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if title and description:
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

@app.route('/instruction')
def instruction():
    return render_template('instruction.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/about')
def about_project():
    return render_template('about.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

# --- Функции работы с сообщениями ---
MESSAGES_FILE = "messages.json"

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_message(message):
    messages = load_messages()
    messages.append(message)
    with open(MESSAGES_FILE, "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)

@app.route("/forum/messages", methods=["POST"])
def post_message():
    user_message = request.form.get("message")
    if user_message:
        save_message({"message": user_message})
        return jsonify({"status": "success", "message": "Сообщение сохранено"})
    return jsonify({"status": "error", "message": "Пустое сообщение"}), 400

if __name__ == "__main__":
    app.run(debug=True)
