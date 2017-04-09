#!/usr/bin/env python3.4
''' main executable file '''

import time
import handlers as Handler

START_TIME = time.time()
Handler.beamauth('main')
Handler.beamauth('bot')
ELAPSED_TIME = time.time() - START_TIME
print(ELAPSED_TIME)
