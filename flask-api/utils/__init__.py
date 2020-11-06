def like_string(s):
    return s + "%"


def construct_results(cursor, data):
    fields = [c[0] for c in cursor.description]
    results = [dict(zip(fields, row)) for row in data]
    print(results)
    return results
