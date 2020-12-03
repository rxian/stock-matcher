from flask import Blueprint, request, abort
from flask import jsonify

from database import connect_db
from utils import construct_results

import listings


@listings.bp.route('/<listing_id>/prices', methods=['GET'])
def get_prices(listing_id):
    """ Get the prices within [start_date, end_date] given a listing_id.

    :raise: 404 Error if no listing with listing_id is found
    :return: 200 if success, with data field in the response body.
    """

    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')

    cursor = connect_db()

    query = "SELECT * FROM Prices WHERE listingID=%s AND date >= %s AND date <= %s"
    cursor.execute(query, (listing_id, start_date, end_date))

    if cursor.rowcount == 0:
        abort(404, 'Listing with id=%s does not exist or does not have any prices listed yet' % (listing_id,))

    data = cursor.fetchall()
    return jsonify({
        "data": construct_results(cursor, data),
    }), 200
