from flask import Flask, render_template, request, abort
from flask_cors import CORS
from models import db, User
from api.user import user_bp
from api.mfa import mfa_bp
from config import Config

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
db.init_app(app)

CORS(
    app, resources={
        r"/api/*": {
            "origins": Config.CORS_ORIGINS.split(","),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600,
        }
    },
)

app.register_blueprint(user_bp)
app.register_blueprint(mfa_bp)

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

def create_example_user():
    user = User.query.filter_by().first()
    if not user:
        user = User(username='admin', email='admin@example.com')
        user.set_password('admin')
        db.session.add(user)
        db.session.commit()
        app.logger.info("Example user created, please change the default credentials!")

def init_db():
    with app.app_context():
        db.create_all()
        create_example_user()
        app.logger.info("Database initialized")

init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
