import logging
import json
import math
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/square', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps(result)


@app.route('/tickerStreamPart1', methods=['POST'])
def to_cumulative():
    result = []
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")
    stream.sort()
    timestamp = stream[0][0:5]
    ticks = []
    tickers = {}
    resultJson = {}
    for i, ele in enumerate(stream):
        if ele[0:5] == timestamp:
            ticker = ele.split(',')
            if ticker[0] not in ticks:
                ticks.append(ticker[0])

            if ticker[1] not in tickers.keys():
                tickers[ticker[1]] = [0, 0]
                tickers[ticker[1]][0] += int(ticker[2])
                notional = int(ticker[2]) * float(ticker[3])
                tickers[ticker[1]][1] += notional
            else:
                tickers[ticker[1]][0] += int(ticker[2])
                notional = int(ticker[2]) * float(ticker[3])
                tickers[ticker[1]][1] += notional

        else:
            for key, value in tickers.items():
                ticks.append(key)
                ticks.append(value[0])
                ticks.append(round(value[1], 1))
            ticks = list(map(str, ticks))
            outputstr = ",".join(ticks)
            result.append(outputstr)
            timestamp = ele[0:5]
            ticks = []

            ticker = ele.split(',')
            if ticker[0] not in ticks:
                ticks.append(ticker[0])
            if ticker[1] not in tickers.keys():
                tickers[ticker[1]] = [0, 0]
                tickers[ticker[1]][0] += int(ticker[2])
                notional = int(ticker[2]) * float(ticker[3])
                tickers[ticker[1]][1] += notional
            else:
                tickers[ticker[1]][0] += int(ticker[2])
                notional = int(ticker[2]) * float(ticker[3])
                tickers[ticker[1]][1] += notional

    for key, value in tickers.items():
        ticks.append(key)
        ticks.append(value[0])
        ticks.append(round(value[1], 1))
    ticks = list(map(str, ticks))
    outputstr = ",".join(ticks)
    result.append(outputstr)
    logging.info("My result :{}".format(result))
    resultJson["output"] = result
    return json.dumps(resultJson)

@app.route('/tickerStreamPart2', methods=['POST'])
def to_cumulative_delayed():
    result = []
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")
    quantity_block = data.get("quantityBlock")
    stream.sort()
    timestamp = stream[0][0:5]
    ticks = []
    tickers = {}
    currenttick = stream[0].split(',')[1]
    isfactor = 0
    currentquantity = 0
    currnotional = 0
    resultJson = {}
    for i, ele in enumerate(stream):
        ticker = ele.split(',')
        if ele[0:5] == timestamp:
            if ticker[1] != currenttick and isfactor > 0:
                isfactor = 0
                ticks.append(currenttick)
                ticks.append(currentquantity)
                ticks.append(round(currnotional, 1))

            if ticker[1] not in tickers.keys():
                tickers[ticker[1]] = [0, 0]
                tickers[ticker[1]][0] += int(ticker[2])
                notional = int(ticker[2]) * float(ticker[3])
                tickers[ticker[1]][1] += notional
                if tickers[ticker[1]][0] % quantity_block == 0:
                    isfactor += 1
                    if ticker[0] not in ticks:
                        ticks.append(ticker[0])
                    currentquantity = tickers[ticker[1]][0]
                    currnotional = tickers[ticker[1]][1]

            else:
                quantity = int(ticker[2])
                while quantity > 0:
                    quantity -= 1
                    tickers[ticker[1]][0] += 1
                    tickers[ticker[1]][1] += float(ticker[3])
                    if tickers[ticker[1]][0] % quantity_block == 0:
                        if ticker[0] not in ticks:
                            ticks.append(ticker[0])
                        currentquantity = tickers[ticker[1]][0]
                        isfactor += 1
                        currnotional = tickers[ticker[1]][1]
            currenttick = ticker[1]


        else:
            if isfactor > 0:
                ticks.append(currenttick)
                ticks.append(currentquantity)
                ticks.append(round(currnotional, 1))
                ticks = list(map(str, ticks))
                outputstr = ",".join(ticks)
                result.append(outputstr)


            timestamp = ele[0:5]
            ticks = []
            isfactor = 0

            if ticker[1] not in tickers.keys():
                tickers[ticker[1]] = [0, 0]
                tickers[ticker[1]][0] += int(ticker[2])
                notional = int(ticker[2]) * float(ticker[3])
                tickers[ticker[1]][1] += notional
                if tickers[ticker[1]][0] % quantity_block == 0:
                    isfactor += 1
                    if ticker[0] not in ticks:
                        ticks.append(ticker[0])
                    currentquantity = tickers[ticker[1]][0]
                    currnotional = tickers[ticker[1]][1]
            else:
                quantity = int(ticker[2])
                while quantity > 0:
                    quantity -= 1
                    tickers[ticker[1]][0] += 1
                    tickers[ticker[1]][1] += float(ticker[3])
                    if tickers[ticker[1]][0] % quantity_block == 0:
                        if ticker[0] not in ticks:
                            ticks.append(ticker[0])
                        currentquantity = tickers[ticker[1]][0]
                        isfactor += 1
                        currnotional = tickers[ticker[1]][1]
            currenttick = ticker[1]

    if isfactor > 0:
        ticks.append(currenttick)
        ticks.append(currentquantity)
        ticks.append(round(currnotional, 1))
        ticks = list(map(str, ticks))
        outputstr = ",".join(ticks)
        result.append(outputstr)
        ticks = []

    if len(ticks) != 0:
        ticks = list(map(str, ticks))
        outputstr = ",".join(ticks)
        result.append(outputstr)
        
    logging.info("My result :{}".format(result))
    resultJson["output"] = result
    return json.dumps(resultJson)

@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()

    logging.info("data sent for evaluation {}".format(data))
    
    database = {1: 4, 2: 4}
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] in database:
                data[i][j] = database[data[i][j]]
                continue
            if math.log2(data[i][j]) == int(math.log2(data[i][j])):
                continue
            else:
                tem_num = [data[i][j]]
                while ((tem_num[-1] not in database) and (math.log2(tem_num[-1]) != int(math.log2(tem_num[-1])))):
                    if tem_num[-1] % 2 == 0:
                        tem_num.append(int(tem_num[-1] / 2))
                    else:
                        tem_num.append(int(tem_num[-1] * 3 + 1))
                if tem_num[-1] in database:
                    tem_num.append(database[tem_num[-1]])
                for n in tem_num:
                    if (n not in database):
                        database[n] = max(tem_num)
                data[i][j] = database[data[i][j]]
    

    logging.info("My result :{}".format(data))

    return json.dumps(data)

@app.route('/calendarDays', methods=['POST'])
def calendarDays():
    data = request.get_json()
    numbers = data.get("numbers")
    numbers[1:] = (i for i in numbers if i > 0 and i < 366)
    return json.dumps(numbers)