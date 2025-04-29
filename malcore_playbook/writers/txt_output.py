import json


def output(out, filename):
    with open(filename, "w") as fh:
        fh.write(str(out))
    return filename
