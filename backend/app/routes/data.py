from flask import Blueprint, jsonify, render_template
from backend.app.services.fred_client import fetch_labour_data

data_bp = Blueprint('data', __name__)

@data_bp.route('/')
def index():
    return render_template('index.html')

@data_bp.route('/api/data/united-states/labour')
def us_labour_data():
    data = fetch_labour_data()
    return jsonify(data)