import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart2', methods=['POST'])
def tickerStreamPart2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")
    quantity_block = data.get("quantityBlock")

    output = []
    h = {}

    previous_time = None

    # first pass
    stream.sort()

    res = ""  # temporary variable to store a string
    for tick in stream:
        time, ticker, qty, price = tick.split(',')
        qty, price = int(qty), float(price)

        if ticker not in h:
            h[ticker] = (0, 0)

        cum_qty, cum_notional = h[ticker]

        leftover_qty = cum_qty % quantity_block

        if leftover_qty + qty >= quantity_block:
            if previous_time is not None:
                if time == previous_time:
                    res += ','
                else:
                    output.append(res)
                    res = time + ','
            else:
                res = time + ','
                previous_time = time

            cut = quantity_block - leftover_qty

            temp_notional = cut * price + cum_notional

            res += f'{ticker},{quantity_block},{round(temp_notional, 1)}'

        new_qty = cum_qty + qty
        new_notional = cum_notional + qty * price

        h[ticker] = (new_qty, new_notional)

    if res:
        output.append(res)

    d = {
        'output': output
    }
    return json.dumps(d)



