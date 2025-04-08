from flask import Flask, send_file, make_response
import matplotlib.pyplot as plt
import io
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/chart/unemployment")
def unemployment_chart():
    # Generate mock unemployment data
    dates = pd.date_range(datetime.today() - timedelta(days=30), periods=30)
    values = np.random.uniform(3.5, 4.5, size=30)

    # Create the chart
    fig, ax = plt.subplots()
    ax.plot(dates, values, label="Unemployment Rate", color="blue")
    ax.set_title("US Unemployment (Mock Data)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Unemployment %")
    ax.legend()

    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    # Build the response with manual CORS header
    response = make_response(send_file(buf, mimetype='image/png'))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True)
