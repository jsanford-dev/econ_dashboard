from flask import Blueprint, jsonify, render_template, abort
from backend.app.services.fred_client import fetch_labour_data

data_bp = Blueprint('data', __name__)

@data_bp.route('/')
def index():
    return render_template('index.html')

@data_bp.route('/api/data/united-states/<topic>')
def us_topic_data(topic):
    if topic == 'labour':
        data = fetch_labour_data()
    elif topic == 'inflation':
        data = {"message": "Inflation data not implemented yet"}
    elif topic == 'yields':
         data = {"message": "Yields data not implemented yet"}
    else:
        abort(404, description="Topic not found")

    return jsonify(data)

