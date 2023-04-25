#Path: server.py
from flask import Flask
from flask import request
from langchain import ChatOpenAI
from scripts.email_generator import email_endpoint

app = Flask(__name__)

@app.route('/server.py', methods=['POST'])
def generate_email_endpoint():
    # Get request data
    data = request.get_json()

    # Call email generator script with data
    result = email_endpoint()

    # Return result
    return result

if __name__ == '__main__':
    app.run(debug=True)
