import redis
import logging
from Models import db
from flask import Flask
from celery import Celery
from config import Config
from flask_mail import Mail
from flask_caching import Cache
from flask_session import Session
from blueprints.user.user import user_bp
from blueprints.roles.role import role_bp
from blueprints.admin.admin import admin_bp
from blueprints.contributor.contributor import contributor_bp

app = Flask(__name__)


app.config.from_object(Config)

app.jinja_env.autoescape = True



# Configure logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='app.log', level=logging.DEBUG, format=log_format)

# Create a logger instance for your application
logger = logging.getLogger(__name__)

#app.config['SECRET_KEY'] = 'your-secret-key'






Session(app)

mail = Mail()
mail.init_app(app)





app.register_blueprint(user_bp) 
app.register_blueprint(role_bp, url_prefix="/role")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(contributor_bp, url_prefix="/contributor")

db.init_app(app)


if __name__ =="__main__":
    app.run(debug=True)
    
