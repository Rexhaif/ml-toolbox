#!/usr/bin/env python
import sys
from notebook.auth import passwd

print(passwd(sys.argv[1]))
