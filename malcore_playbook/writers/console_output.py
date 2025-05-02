#  Copyright (c) 2025.
#  Penetrum LLC (all rights reserved)
#  Copyright last updated: 5/2/25, 10:29 AM
#
#

import json


def output(out, filename):
    if isinstance(out, str):
        return f"\n{'*' * 63}\n{out}\n{'*' * 63}"
    else:
        return f"\n{'*' * 63}\n{json.dumps(out['data'], indent=2)}\n{'*' * 63}"

