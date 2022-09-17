from flask import Flask
import logging
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
import codeitsuisse.routes.square
import codeitsuisse.routes.tickerStreamPart1
import codeitsuisse.routes.tickerStreamPart2
import codeitsuisse.routes.travelling_suisse_robot



