# TODO: finish the comment.
from flask import abort


def like_string(s):
    """
    :param s:
    :return:
    """
    return s + "%"


def construct_result(cursor, data):
    fields = [c[0] for c in cursor.description]
    return dict(zip(fields, data))


def construct_results(cursor, data):
    """
    :param cursor:
    :param data:
    :return:
    """
    fields = [c[0] for c in cursor.description]
    return [dict(zip(fields, row)) for row in data]


def check_json(json, keys):
    """ Check whether the json body in request contains all required keys
    :param json: the json object
    :param keys: the keys to check
    :return 400 if there are some missing key
    :return None if OK
    """
    if json is None:
        abort(400, 'No JSON object provided')
    for key in keys:
        if key not in json:
            abort(400, 'Missing key %s in JSON' % key)
