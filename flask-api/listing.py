from flask import Blueprint
from flask import jsonify

from database import mysql

listing = Blueprint('listing', __name__)


@listing.route('/', methods=['GET'])
def get_stock():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Listings")
    data = cursor.fetchone()

    return jsonify({
        "data": data,
    })
