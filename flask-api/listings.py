from flask import Blueprint, request, abort
from flask import jsonify

from database import mysql
from utils import like_string, construct_results, check_json

bp = Blueprint('listings', __name__)

import sys
sys.path.append('../sql')
import queries

@bp.route('/', methods=['GET'])
def get_listings():
    """ Get all listings with or without a keyword

    If a keyword is given, this method will return all listings with "symbol" attribute prefixed with the keyword.
    Otherwise, all listings are returned.

    The keyword should be given as a parameter. Example: http://localhost:5000/api/listings?keyword=A

    :raise: 404 Error if no listing is found
    :return: 200 if success, with data field in the response body.
    """
    cursor = connect_db()

    prefix = request.args.get('keyword')

    data = queries.getSymbols(prefix)

    if not data:
        abort(404, 'No suggestions')

    return jsonify({
        "data": construct_results(cursor, data),
    }), 200


@bp.route('/<listing_id>', methods=['GET'])
def get_listing(listing_id):
    """ Get the listing detail given a listing_id

    :raise: 404 Error if no listing with listing_id is found
    :return: 200 if success, with data field in the response body.
    """

    cursor = connect_db()

    query = "SELECT * FROM Listings WHERE listingID=%s"
    cursor.execute(query, (listing_id,))

    if cursor.rowcount == 0:
        abort(404, 'Listing with id=%s does not exist' % (listing_id,))

    data = cursor.fetchone()
    return jsonify({
        "data": construct_results(cursor, [data]),
    }), 200


# TODO: double check database schema: are these fields required? Are active, tracked default to 1, 0?
@bp.route('/', methods=["POST"])
def create_listing():
    """ Create a listing record in the database

    Following fields are accepted:
    - symbol (required)
    - name
    - active (default to 1)
    - tracked (default to 0)

    :raise: 400 if the request does not contain all required fields
    :raise: 400 if the operation fails
            Some possible causes may include: listingID already exists in the database, illegal symbol, etc.
    :return: 201 if success, along with data field in the response body
    """

    req = request.get_json()
    check_json(req, ["symbol"])

    print(req)

    symbol = req['symbol']
    name = req['name'] if 'name' in req else None
    active = req['active'] if 'active' in req else None
    tracked = req['tracked'] if 'tracked' in req else None

    # cursor = connect_db()
    # query = "INSERT INTO Listings(symbol, name) VALUES (%s, %s)"
    # res = cursor.execute(query, (symbol, name))

    # print(cursor.fetchone())
    # print(res)

    return jsonify({
        "data": None
    }), 200


@bp.route('/<listing_id>', methods=['PUT'])
def update_listing(listing_id):
    """ Replace a listing detail with the given data

    The body should contain the following information:
    - symbol
    - name
    - active
    - tracked

    All fields must be provided.

    :raise 400 Error if the update fails, either because the database operation fail, or some fields are not provided
    :raise 404 Error if no listing with listing_id is found
    :return 200 if success, with updated data given in the data field in the response body.
    """

    req = request.get_json()
    check_json(req, ["symbol", "name", "active", "tracked"])

    symbol_new = req["symbol"]
    name_new = req["name"]
    active_new = req["active"]
    tracked_new = req["tracked"]

    cursor = connect_db()
    query = "UPDATE Listings SET symbol=%s, name=%s, active=%s, tracked=%s"
    cursor.execute(query, (symbol_new, name_new, active_new, tracked_new))

    return jsonify({
        "data": None,
    }), 200


@bp.route('/<listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    return jsonify({
        "data": None
    }), 200


def connect_db():
    conn = mysql.connect()
    return conn.cursor()
