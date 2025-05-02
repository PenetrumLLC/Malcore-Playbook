#  Copyright (c) 2025.
#  Penetrum LLC (all rights reserved)
#  Copyright last updated: 5/2/25, 10:29 AM
#
#

import json


def output(out, filename):
    with open(filename, "w") as fh:
        fh.write(str(out))
    return filename
