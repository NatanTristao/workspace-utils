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
    return render_template('index.html')

@app.route('/defesa_facil')
def defesa_facil():
    return render_template('defesa_facil.html', image_generated=False)

@app.route('/seminar_art_generator')
def seminar_art_generator():
    return render_template('seminar_art_generator.html', image_generated=False)

@app.route('/drive')
def go_to_drive():
    return redirect('https://drive.google.com/drive/u/0/my-drive', code=302)

@app.route('/canva')
def go_to_canva():
    return redirect('https://www.canva.com/', code=302)

@app.route('/senhas')
def passwords():
    return redirect('https://drive.google.com/file/d/11oreuaEYvus529albJyRa7Y_ToLcCRP_/view?usp=sharing', code=302)

@app.route('/totem')
def totem_visualization():
    return redirect('https://www.inf.ufrgs.br/totem/?preview=true&showImages=true', code=302)

@app.route('/manual')
def manuel():
    return redirect('#', code=302)

########### FUNÇÃO USADA PARA O GERADOR DE SEMINÁRIOS ##########
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


########### FUNÇÃO USADA PARA O GERADOR DE DEFESAS ##########
@app.route('/generate_defesa', methods=['POST'])
def generate_defesa(): 
    data = {
        "degree_type":    request.form['degree_type'],   
        "course":         request.form['course'],         
        "candidate_name": request.form['candidate_name'], 
        "advisor":        request.form['advisor'],        
        "coadvisor":      request.form.get('coadvisor', ''),   
        "title":          request.form['title'],         
        "date":           request.form['date'],           
        "time":           request.form['time'],          
        "stream_link":    request.form.get('stream_link', ''), 
        "observation":    request.form.get('observation', ''), 
    }

    flash('Arte de defesa gerada com sucesso!')
    return render_template(
        'defesa_facil.html',
        image_generated=True,
        image_url=url_for('static', filename=f'outputs/{output_filename}') 
        )

if __name__ == '__main__':
    app.run(debug=True)
