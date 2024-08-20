from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            service TEXT,
            action TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Welcome Message Endpoint
@app.route('/welcome', methods=['GET'])
def welcome():
    return jsonify({
        'message': "Hi there! I'm here to help you connect with top-rated contractors. How can I assist you today?"
    })

# Capture Lead Information Endpoint
@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    service = data.get('service')
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO leads (name, email, phone, service, action) VALUES (?, ?, ?, ?, ?)',
              (name, email, phone, service, ""))
    conn.commit()
    conn.close()
    
    return jsonify({
        'message': "Thank you! Your information has been captured. How would you like to proceed?",
        'options': ['Fill in a Form', 'Call a Contractor', 'Set an Appointment']
    })

# Handle Service Action Selection
@app.route('/action', methods=['POST'])
def action():
    data = request.json
    name = data.get('name')
    action = data.get('action')
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE leads SET action = ? WHERE name = ?', (action, name))
    conn.commit()
    conn.close()
    
    response = {}
    if action == 'Fill in a Form':
        response = {'message': " wonder contractor."}
    elif action == 'Call a Contractor':
        response = {'message': "Here are some phone numbers you can call."}
    elif action == 'Set an Appointment':
        response = {'message': "Let's set an appointment with your chosen contractor."}

    return jsonify(response)

# Serve Chat Interface
@app.route('/')
def index():
    return render_template('chatbot.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
