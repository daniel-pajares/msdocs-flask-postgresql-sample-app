import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from flask import jsonify


app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue
from models import ImagenProcesada

@app.route('/', methods=['GET'])
def index():
    imagenes = ImagenProcesada.query.order_by(ImagenProcesada.fecha.desc()).all()

    imagenes_preparadas = []
    for img in imagenes:
        imagenes_preparadas.append({
            "id": img.id,
            "name": img.name,
            "fecha": img.fecha.strftime("%Y-%m-%d %H:%M"),
            "usuario": img.usuario,
            "fases": img.fases.split(', '),
            "pixeles": img.pixeles
        })

    return render_template('index.html', images=imagenes_preparadas)

@app.route('/<int:id>', methods=['GET'])
def details(id):
    img = ImagenProcesada.query.get(id)
    if img is None:
        return "Imagen no encontrada", 404

    image = {
        "id": img.id,
        "name": img.name,
        "fecha": img.fecha.strftime("%Y-%m-%d %H:%M"),
        "usuario": img.usuario,
        "fases": img.fases.split(', '),
        "pixeles": img.pixeles
    }

    return render_template('details.html', image=image)

# Ruta POST /api/upload para recibir desde Scala
@app.route('/api/upload', methods=['POST'])
@csrf.exempt
def upload_image_data():
    data = request.get_json()

    try:
        imagen = ImagenProcesada(
            name=data['name'],
            usuario=data['usuario'],
            fecha=datetime.fromisoformat(data['fecha']),
            fases=', '.join(data['fases']),
            pixeles=data['pixeles']
        )

        db.session.add(imagen)
        db.session.commit()
        return jsonify({"message": "Imagen guardada correctamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run()
