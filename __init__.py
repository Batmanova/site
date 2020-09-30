from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from flask_login import LoginManager
#from config import basedir
from dateutil.parser import parse

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(Config)
db = SQLAlchemy(app)
#migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/microblog.txt', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

from app import routes, models


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt is None:
        fmt = '%d.%m.%Y'
    return date.strftime(fmt)


db.create_all()
db.session.commit()
