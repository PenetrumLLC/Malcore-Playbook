#  Copyright (c) 2025.
#  Penetrum LLC (all rights reserved)
#  Copyright last updated: 5/2/25, 12:59 PM
#
#

import json


def output(out, filename):
    if not isinstance(out, dict):
        out = {"output": out}
    with open(filename, 'w') as fh:
        json.dump(out, fh, indent=4)
    return filename
