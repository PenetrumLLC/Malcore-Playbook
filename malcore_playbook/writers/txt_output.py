#  Copyright (c) 2025.
#  Penetrum LLC (all rights reserved)
#  Copyright last updated: 4/22/25, 11:18 AM
#

import json


def output(out, filename):
    with open(filename, "w") as fh:
        fh.write(str(out))
    return filename
