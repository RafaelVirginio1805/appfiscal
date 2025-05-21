from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    provedor = request.form['provedor']
    poste = request.form['poste']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    obs = request.form['obs']

    # Foto
    foto = request.files['foto']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{provedor}_{timestamp}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    foto.save(filepath)

    # Aqui você poderia salvar no MySQL, por enquanto salva no terminal
    print(f"Provedor: {provedor}")
    print(f"Poste: {poste}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print(f"Observações: {obs}")
    print(f"Foto salva em: {filepath}")

    return f"<h2>Dados recebidos com sucesso!</h2><a href='/'>Voltar</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
