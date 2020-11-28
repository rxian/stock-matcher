from flask import Blueprint, request, abort
from flask import jsonify

from news_api import get_article_list
from utils import construct_results, check_json, construct_result

bp = Blueprint('news', __name__)


@bp.route('/<listing_id>', methods=['GET'])
def get_news_mentioning_listing(listing_id):
    result = get_article_list(int(listing_id), 10)
    return jsonify({
        "data": result
    }), 200
