#  Copyright (c) 2025.
#  Penetrum LLC (all rights reserved)
#  Copyright last updated: 4/22/25, 11:15 AM
#

import json


def output(out, filename):
    with open(filename, 'w') as fh:
        json.dump(out, fh, indent=4)
    return filename
