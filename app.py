from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)
SHARED_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads', 'flask_hopping_project', 'shared_data')
os.makedirs(SHARED_FOLDER, exist_ok=True)

FLAGS_FILE = os.path.join(SHARED_FOLDER, 'simulation_flags.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_text', methods=['POST'])
def encrypt_text():
    text = request.form['text']
    key = 'eceproject2025'
    encrypted = bytearray()

    for i, char in enumerate(text):
        encrypted_char = ord(char) ^ ord(key[i % len(key)])
        encrypted.append(encrypted_char)

    TEXT_FILE = os.path.join(SHARED_FOLDER, 'text_message.txt')  # ✅ Add this line
    with open(TEXT_FILE, 'wb') as f:
        f.write(encrypted)

    return 'Text encrypted and saved successfully.'


@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return "No audio file part", 400
    audio = request.files['audio']
    audio.save(os.path.join(SHARED_FOLDER, 'uploaded_audio.wav'))
    return "Audio uploaded", 200

@app.route('/set_simulation_flags', methods=['POST'])
def set_simulation_flags():
    data = request.get_json()
    flags = {
        "simulate_jamming": data.get("simulate_jamming", False),
        "simulate_eavesdropping": data.get("simulate_eavesdropping", False)
    }
    with open(FLAGS_FILE, 'w') as f:
        json.dump(flags, f)
    return jsonify({"status": "flags saved"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's port if provided, otherwise default to 5000
    app.run(host='0.0.0.0', port=port)