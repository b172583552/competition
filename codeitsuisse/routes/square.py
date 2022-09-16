import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart1', methods=['POST'])
#def evaluate():
    #data = request.get_json()
    #logging.info("data sent for evaluation {}".format(data))
    #inputValue = data.get("input")
    #result = inputValue * inputValue
    #logging.info("My result :{}".format(result))
    #return json.dumps(result)

def to_cumulative(stream: list):
    # Assume the information of every product will be returned at each second even though there is no update information at that second
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")

    newls = []
    stream.sort()
    for i in stream:
        unit = i.split(',')
        newls.append(unit)
    result = {}
    n = 0  # index of total line
    comptime = newls[0][0]
    ls = []
    while (n < len(stream)):
        checktime = newls[n][0]
        checkticker = newls[n][1]
        newls[n][2] = int(newls[n][2])
        newls[n][3] = float(newls[n][3])
        if (checktime == comptime):  # not upgrading time
            if checkticker not in result:
                result[checkticker] = [newls[n][2], newls[n][3] * newls[n][2]]
            elif checkticker in result:
                result[checkticker][0] += newls[n][2]  # add quantity
                result[checkticker][1] += newls[n][3] * newls[n][2]  # add notional
        else:  # upgrade a new time
            re = newls[n - 1][0]  # print previous record first
            for ticker in result:
                re = re + ',' + ticker + ',' + str(result[ticker][0]) + ',' + str(result[ticker][1])
            ls.append(re)
            if checkticker not in result:
                result[checkticker] = [newls[n][2], newls[n][3] * newls[n][2]]
            elif checkticker in result:
                result[checkticker][0] += newls[n][2]  # add quantity
                result[checkticker][1] += newls[n][3] * newls[n][2]  # add notional
        comptime = newls[n][0]
        n += 1
    re = newls[n - 1][0]
    for ticker in result:
        re = re + ',' + ticker + ',' + str(result[ticker][0]) + ',' + str(result[ticker][1])
    ls.append(re)
    last_out={}
    last_out["output"]=ls

    logging.info("My result :{}".format(last_out))
    return json.dumps(last_out)

    raise Exception


@app.route('/tickerStreamPart2', methods=['POST'])
def to_cumulative_delayed(stream: list, quantity_block: int):
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")
    quantity_block = data.get("quantityBlock")

    # Assume only the product which fulfill the block requirements at each specific second will be returned at that second
    newls = []
    stream.sort()
    for i in stream:
        unit = i.split(',')
        newls.append(unit)
    database = {}
    n = 0
    block = quantity_block
    pre_t = ''
    while (n < len(newls)):
        time = newls[n][0]
        quantity = int(newls[n][2])
        price = float(newls[n][3])
        if time not in database:
            database[time] = {}
        product = newls[n][1]
        if product not in database[time]:
            database[time][product] = []
        if (pre_t == ''):
            database[time][product] = [quantity, quantity * price, price]
        else:
            for t in database:
                if (product in database[t]) and (t != time):
                    pre_t = t
            pre_q = database[pre_t][product][0]
            pre_n = database[pre_t][product][1]
            database[time][product] = [pre_q + quantity, pre_n + quantity * price, price]
        if (n + 1 < len(newls)):
            next_t = newls[n + 1][0]
        if (next_t != time):
            pre_t = time
        n += 1
    block_d = {}
    for time in database:
        for product in database[time]:
            if product not in block_d:
                block_d[product] = 0
    out = []
    for time in database:
        e = time
        for product in database[time]:
            if (database[time][product][0] // block) != block_d[product]:
                q = database[time][product][0] // block * block
                remainder = database[time][product][0] % block
                n = database[time][product][1] - database[time][product][2] * remainder
                e = e + ',' + product + ',' + str(q) + ',' + str(n)
                block_d[product] = database[time][product][0] // block
        if (e != time):
            out.append(e)

    lastlast_out = {}
    lastlast_out["output"] = out

    logging.info("My result :{}".format(lastlast_out))
    return json.dumps(lastlast_out)

    raise Exception


