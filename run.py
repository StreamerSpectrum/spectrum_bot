#!/usr/bin/env python3
''' Main program '''

import time
from handlers import BeamOAuth

START_TIME = time.time()
BeamOAuth.initialize()
ELAPSED_TIME = time.time() - START_TIME
print(ELAPSED_TIME)
