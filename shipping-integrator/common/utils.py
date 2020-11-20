import json


def class_to_json(classes):
    string = json.dumps(classes, default=lambda o: o.__dict__)
    return json.loads(string)
