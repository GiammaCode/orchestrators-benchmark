from bson.json_util import dumps

def bson_to_json(data):
    """
    Convert BSON data (ObjectId e ISODate) in JSON strings.
    """
    return dumps(data)
