from flask import Flask, render_template, send_from_directory, request, jsonify

import os
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/accoun_summary/")
def account_summary():
    filepath = "/Users/guoziting/Desktop/capychain/"
    return send_from_directory(filepath, "account_summary_demo_2.pdf")

@app.route("/tax_return/")
def tax_return():
    filepath = "/Users/guoziting/Desktop/capychain/"
    return send_from_directory(filepath, "form_8949.pdf")

@app.route('/process-data', methods=['POST'])
def process_data():
    # Access the data sent from the frontend
    data = request.json

    print("data: ", data)
    # Perform data processing
    result = str(data) + ' processed'

    # Return a response
    return jsonify({'result': result})

# if __name__ == "__main__":
#     app.run(debug=True, port=8000)