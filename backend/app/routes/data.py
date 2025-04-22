from flask import Blueprint, jsonify, render_template, abort
from backend.app.services.fred_client import fetch_us_overview_data


data_bp = Blueprint('data', __name__)

@data_bp.route('/')
def index():
    return render_template('index.html')

@data_bp.route('/api/data/united-states/overview')
def us_overview_data():
    data = fetch_us_overview_data()
    return jsonify(data)

@data_bp.route('/api/data/united-states/<topic>')
def us_topic_data(topic):
    if topic == 'labour':
        data = {"message": "Labour data not implemented yet"}
    elif topic == 'inflation':
        data = {"message": "Inflation data not implemented yet"}
    elif topic == 'yields':
         data = {"message": "Yields data not implemented yet"}
    else:
        abort(404, description="Topic not found")

    return jsonify(data)

