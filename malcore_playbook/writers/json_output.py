import json


def output(out, filename):
    with open(filename, 'w') as fh:
        json.dump(out, fh, indent=4)
    return filename
