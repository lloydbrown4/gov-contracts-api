from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/contracts')
def get_contracts():
    return jsonify([
        {"header": "Test Contract", "sub_header": "Example Subheader", "contract_value": "£100,000"}
    ])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


