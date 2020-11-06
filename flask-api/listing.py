from flask import Blueprint, request
from flask import jsonify

from database import mysql
from utils import like_string, construct_results

listing = Blueprint('listing', __name__)


@listing.route('/', methods=['GET'])
def listings():
    conn = mysql.connect()
    cursor = conn.cursor()

    keyword = request.args.get('keyword')

    query = "SELECT * FROM Listings WHERE symbol LIKE %s"
    cursor.execute(query, (like_string(keyword),))

    data = cursor.fetchall()

    return jsonify({
        "data": construct_results(cursor, data),
    }), 200
