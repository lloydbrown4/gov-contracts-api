from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS (app)

@app.route('/api/contracts')
def get_contracts():
    base_url = "https://www.contractsfinder.service.gov.uk/Search/Results?page="
    headers_list, sub_headers_list, values_list = [], [], []

    page = 1
    while True:
        response = requests.get(base_url + str(page))
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".search-result")
        if not results:
            break

        for result in results:
            h = result.select_one(".search-result-header a")
            sh = result.select_one(".search-result-sub-header")
            val = ""
            for dt in result.find_all("dt"):
                if "Value of contract" in dt.text:
                    val_tag = dt.find_next_sibling("dd")
                    val = val_tag.text.strip() if val_tag else ""

            headers_list.append(h.text.strip() if h else "")
            sub_headers_list.append(sh.text.strip() if sh else "")
            values_list.append(val)

        page += 1

    contracts = [
        {"header": h, "sub_header": sh, "contract_value": val}
        for h, sh, val in zip(headers_list, sub_headers_list, values_list)
    ]

    return jsonify(contracts)

if __name__ == '__main__':
    app.run(debug=True)
