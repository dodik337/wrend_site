# taskkill /f /im python.exe
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html', title='1')

if __name__ == '__main__':
    app.run(debug=True)
