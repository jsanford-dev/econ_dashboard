from flask import Blueprint, jsonify, render_template, abort
from backend.app.services.fred_client import fetch_us_overview_data_cached


data_bp = Blueprint('data', __name__)

@data_bp.route('/')
def index():
    return render_template('index.html')

@data_bp.route('/united-states/overview')
def united_states_overview():
    data = fetch_us_overview_data_cached()
    return render_template('us_overview.html', data=data)

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

