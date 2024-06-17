# app.py
import os  # Import the os module

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Heroku!"

if __name__ == '__main__':
    # Use os.environ.get() to retrieve the PORT environment variable provided by Heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
