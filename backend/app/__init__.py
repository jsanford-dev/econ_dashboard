from flask import Flask
import os
from backend.app.routes.data import data_bp
from backend.app.filters import clean_label

def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, '..', '..', 'frontend', 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, '..', '..', 'frontend', 'static')

    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR
    )

    app.register_blueprint(data_bp)

    # Filters for US overview page
    app.jinja_env.filters['clean_label'] = clean_label 

    return app