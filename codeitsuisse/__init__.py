import os
import sys
import logging
from flask import Flask

app = Flask(__name__)
if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)

import codeitsuisse.routes.square
import codeitsuisse.routes.tickerStreamPart1
import codeitsuisse.routes.tickerStreamPart2
import codeitsuisse.routes.travelling_suisse_robot





