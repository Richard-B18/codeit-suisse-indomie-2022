import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/tickerStreamPart1', methods=['POST'])
def tickerStreamPart1():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")

    output = []
    h = {}

    previous_time = None
    previous_ticker = None

    # first pass
    stream.sort()

    res = ""  # temporary variable to store a string
    for tick in stream:
        time, ticker, qty, price = tick.split(',')
        qty, price = int(qty), float(price)

        if ticker not in h:
            h[ticker] = (0, 0)

        if previous_time is not None:
            if time != previous_time:
                output.append(res)

                # restart the output string
                res = time + ','
                previous_time = time
            else:
                res += ','
        # first loop
        else:
            res = time + ','
            previous_time = time

        cum_qty, cum_notional = h[ticker]

        new_qty = cum_qty + qty
        new_notional = cum_notional + qty * price

        h[ticker] = (new_qty, new_notional)

        res += f'{ticker},{new_qty},{round(new_notional, 1)}'

    output.append(res)

    d = {
        'output': output
    }

    return json.dumps(d)
