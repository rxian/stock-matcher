import flask
from flask_cors import CORS
from config import app_config
from database import mysql
from listing import listing

# app configs
# TODO: set development/production flag from cli
app = flask.Flask(__name__)
app.config.from_object(app_config['development'])
app.register_blueprint(listing, url_prefix="/api/listing")

CORS(app)

mysql.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
