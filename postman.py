from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    # Fetching the data exactly like your script did
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    leads = response.json()
    return render_template('postman.html', leads=leads)

if __name__ == '__main__':
    app.run(debug=True)