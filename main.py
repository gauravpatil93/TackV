# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, render_template, request
import requests
import json

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
BASE_CURRENCY = 'USD'


@app.route('/')
def index():
    response = requests.get('https://api.exchangeratesapi.io/latest?base='+BASE_CURRENCY)
    if response.status_code == 200:
        return render_template("exchange_rates.html", codes=list(response.json()["rates"].keys()), title="Currency Exchange - Gaurav Patil", eur=response.json()["rates"]['EUR'])
    else:
        return "Error establishing connection to the API"


@app.route('/getexchangerate', methods=["POST"])
def exchange_rates():
    if request.method == "POST":
        base_code = request.json['base_code']
        target_code = request.json['target_code']
        amount = request.json['amount']
        response = requests.get('https://api.exchangeratesapi.io/latest?base='+base_code)
        if response.status_code == 200:
            exchange_rate_data = response.json()["rates"]
            return json.dumps({
                'source_code': base_code,
                'target_code': target_code,
                'source_amount_base': 1,
                'target_amount_base': exchange_rate_data[target_code],
                'source_amount': amount,
                'target_amount': str(float(amount) * exchange_rate_data[target_code]) if amount.isdigit() or amount.replace(".", "").isdigit() else "Invalid input"
            })
        else:
            return "Error establishing connection to the API"


@app.route('/getexchangerateall', methods=["POST"])
def exchange_rates_all():
    if request.method == "POST":
        base_code = request.json['base_code']
        amount = request.json['amount']
        response = requests.get('https://api.exchangeratesapi.io/latest?base='+base_code)
        if response.status_code == 200:
            exchange_rate_data = response.json()["rates"]
            list_of_dicts = []
            for code, rate in exchange_rate_data.items():
                list_of_dicts.append({
                    'base': base_code,
                    'target': code,
                    'exchange': rate,
                    'conversion': str(float(amount) * exchange_rate_data[code]) if amount.isdigit() or amount.replace(".", "").isdigit() else "Invalid input"
                })

            return json.dumps(sorted(list_of_dicts, key = lambda i: i['exchange']) )
        else:
            return "Error establishing connection to the API"


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
