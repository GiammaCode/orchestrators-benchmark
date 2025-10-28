from bson.json_util import dumps

def bson_to_json(data):
    """Converte dati BSON (come ObjectId e ISODate) in stringhe JSON."""
    return dumps(data)
