from flask import Flask, request, render_template, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from Seminar_Art_Generator import generate_art

app = Flask(__name__)
app.secret_key = 'secret'

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html', image_generated=False)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.to_dict()
    file = request.files['photo']
    filename = secure_filename(file.filename)
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(photo_path)

    json_data = {
        "date": data['date'],
        "time": data['time'],
        "duration": data['duration'],
        "title": data['title'],
        "speaker": data['speaker'],
        "stream_link": data['stream_link'],
        "location": data.get('location', ''),
        "observation": data.get('observation', ''),
        "highlight_color": data.get('highlight_color', '#ffe6c8'),
        "photo": filename
    }

    generate_art(json_data, output_path=app.config['OUTPUT_FOLDER'], upload_path=app.config['UPLOAD_FOLDER'])

    flash('Imagem gerada com sucesso!')
    return render_template('index.html', image_generated=True, image_url=url_for('static', filename='outputs/seminar_art.png'))

if __name__ == '__main__':
    app.run(debug=True)
