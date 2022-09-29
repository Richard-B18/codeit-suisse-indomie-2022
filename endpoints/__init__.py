from flask import Flask

app = Flask(__name__)

import endpoints.routes.square
import endpoints.routes.example
