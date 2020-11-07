import flask
from flask_cors import CORS
from config import app_config
from database import mysql
import listings

# app configs
# TODO: set development/production flag from cli
app = flask.Flask(__name__)
app.config.from_object(app_config['development'])
app.register_blueprint(listings.bp, url_prefix="/api/listings")

CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

mysql.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
