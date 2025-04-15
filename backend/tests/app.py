from flask import Flask, send_file, make_response
from test_nfp import ProcessData
from fredapi import Fred
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load FRED API key and fetch data once at startup
load_dotenv()
fred = Fred(api_key=os.getenv("FRED_API_KEY"))
data = fred.get_series('USPRIV')
recession = fred.get_series('USREC')

@app.route("/chart/non_farm_payrolls")
def non_farm_payroll_chart():
    processor = ProcessData(data, recession)
    chart_buf = processor.generate_chart_buffer()

    response = make_response(send_file(chart_buf, mimetype='image/png'))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True)