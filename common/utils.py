import json
import dicttoxml


def json_to_xml(json, custom_root, cdata=False):
    # Name of parent tag for a list item
    def item_func(x):
        return "piece"

    xml = dicttoxml.dicttoxml(
        json,
        item_func=item_func,
        custom_root=custom_root,
        attr_type=False,
        cdata=cdata,
    )

    return xml


def class_to_json(classes):
    string = json.dumps(classes, default=lambda o: o.__dict__)
    return json.loads(string)
