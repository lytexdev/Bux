from flask import Flask, render_template
from config import Config

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.after_request
def add_header(response):
    response.headers['X-Robots-Tag'] = 'noindex, nofollow'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
