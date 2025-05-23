from flask import Flask, render_template, request
import os
from datetime import datetime
import mysql.connector

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/enviar', methods=['GET','POST'])
def enviar():
    provedores_raw = request.form['provedor']
    poste = request.form['poste']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    obs = request.form.get('obs', '')

    # Foto
    foto = request.files['foto']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    foto_path = None

    if foto:
        filename = f"foto_{timestamp}.jpg"
        foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(foto_path)

    # Divide os provedores por vírgula
    provedores = [p.strip() for p in provedores_raw.split(',') if p.strip()]

    for provedor in provedores:
        print(f"Provedor: {provedor}")
        print(f"Poste: {poste}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Observações: {obs}")
        print(f"Foto salva em: {foto_path}")
        salvar_no_banco(provedor, poste, latitude, longitude, obs, foto_path)

    return f"<h2>{len(provedores)} provedor(es) registrado(s) com sucesso!</h2><a href='/'>Voltar</a>"

def salvar_no_banco(provedor, poste, latitude, longitude, obs, foto_path):
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='app_fiscal'
        )

        cursor = conexao.cursor()
        query = """
            INSERT INTO registros (provedor, poste, latitude, longitude, obs, foto_path, data_hora)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        valores = (provedor, poste, latitude, longitude, obs, foto_path)
        cursor.execute(query, valores)
        conexao.commit()
        cursor.close()
        conexao.close()
        print("Dados inseridos com sucesso no banco.")
    except mysql.connector.Error as err:
        print(f"Erro ao conectar/inserir no MySQL: {err}")

# ⛔️ Aqui estava o erro: isso precisa ficar fora de qualquer função!
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
