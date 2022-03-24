from flask import Flask
from flask_wtf import CSRFProtect
from core.models import db
import logging

app = Flask(__name__)
app.config.from_object('config.Config')

# import after app to prevent circular dependency
import core.views

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

db.init_app(app)
with app.app_context():
    db.create_all()

csrf = CSRFProtect(app)
csrf.init_app(app)







