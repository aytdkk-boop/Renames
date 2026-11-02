from flask import Flask, request, jsonify
import pyotp, time, os

app = Flask(__name__)

# Читаем HTML из той же папки
@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/code', methods=['POST'])
def get_code():
    data = request.get_json()
    secret = (data.get('secret') or '').strip()
    if not secret:
        return jsonify({'error': 'Пустой ключ'}), 400
    try:
        totp = pyotp.TOTP(secret)
        code = totp.now()
        left = 30 - (int(time.time()) % 30)
        return jsonify({'code': code, 'seconds_left': left})
    except Exception as e:
        return jsonify({'error': 'Неверный ключ'}), 400

# Эта часть нужна для Render / хостинга
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))