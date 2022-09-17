import logging
import json
import math
from flask import request, jsonify

from codeitsuisse import app
import datetime
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
    #result = []
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    #int_ls = data.get("stream")
    """
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
    #resultJson["output"] = result
    """
    return json.dumps(data)



@app.route('/calendarDays', methods=['POST'])
def calendarday():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    data_ls = data.get("numbers")


    y=data_ls[0]
    result=[]
    #convert number to string like "2022-01-01-5" and make them in a list
    for i in range(1, len(data_ls)):
        day = data_ls[i]
        first_day = datetime.date(y, 1, 1)
        wanted_day = first_day + datetime.timedelta(day - 1)
        week = datetime.datetime.weekday(wanted_day)
        wanted_day = str(wanted_day) + '-' + str(week+1)
        result.append(wanted_day)

    # judge
    if result == []:
        out = "       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,"
        out2=[2001]
        resultJson = {}
        logging.info("My result :{}".format(resultJson))
        resultJson["part1"] = out
        resultJson["part2"] = out2
        return json.dumps(resultJson)

    week_info = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
    for d in result:
        year=d[0:4]
        if int(year)!=y:
            continue
        week = int(d[11:])
        month = d[5:7]
        if month[0] == '0':
            month = int(month[-1])
        elif month == '10':
            month = 10
        elif month == '11':
            month = 11
        elif month == '12':
            month = 12
        week_info[month].append(week)



    out=""
    for key in week_info:
        if (week_info[key]==[]):
            out=out+"       ,"
        elif (1 in week_info[key]) and (2 in week_info[key]) and (3 in week_info[key]) and (4 in week_info[key]) and (5 in week_info[key]) and (6 in week_info[key]) and (7 in week_info[key]) :
            out=out+"alldays,"
        elif (1 not in week_info[key]) and (2 not in week_info[key]) and (3 not in week_info[key]) and (4 not in week_info[key]) and (5 not in week_info[key]) and (6 in week_info[key]) and (7 in week_info[key]) :
            out = out + "weekend,"
        elif (1 in week_info[key]) and (2 in week_info[key]) and (3 in week_info[key]) and (4 in week_info[key]) and (5 in week_info[key]) and (6 not in week_info[key]) and (7 not in week_info[key]) :
            out=out+"weekday,"
        else:
            temp=""
            if (1 in week_info[key]):
                temp+="m"
            else:
                temp+=" "
            if (2 in week_info[key]):
                    temp += "t"
            else:
                    temp += " "
            if (3 in week_info[key]):
                temp+="w"
            else:
                temp+=" "
            if (4 in week_info[key]):
                temp+="t"
            else:
                temp+=" "
            if (5 in week_info[key]):
                temp+="f"
            else:
                temp+=" "
            if (6 in week_info[key]):
                temp+="s"
            else:
                temp+=" "
            if (7 in week_info[key]):
                temp+="s"
            else:
                temp+=" "
            out=out+temp+','






    str_info = out

    for i in range(0, len(str_info)):
        if str_info[i] == ' ':
            break
        i += 1
    year = i + 2001

    date_ls = str_info.split(',')
    week_info = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
    for m in range(1, 13):  # month
        month_info = date_ls[m - 1]  # a string contains some characters
        if month_info == "alldays":
            week_info[m] = [1, 2, 3, 4, 5, 6, 7]
        elif month_info == "weekend":
            week_info[m] = [6, 7]
        elif month_info == "weekday":
            week_info[m] = [1, 2, 3, 4, 5]
        elif month_info == "       ":
            week_info[m] = []
        else:
            if month_info[0] != ' ':
                week_info[m].append(1)
            if month_info[1] != ' ':
                week_info[m].append(2)
            if month_info[2] != ' ':
                week_info[m].append(3)
            if month_info[3] != ' ':
                week_info[m].append(4)
            if month_info[4] != ' ':
                week_info[m].append(5)
            if month_info[5] != ' ':
                week_info[m].append(6)
            if month_info[6] != ' ':
                week_info[m].append(7)

    out2 = [year]
    first_day_of_year = datetime.date(year, 1, 1)
    for m in week_info:
        first_day= datetime.date(year, m, 1)
        week = datetime.datetime.weekday(first_day)
        for i in week_info[m]:
            delta = i + 7 - week - 1
            wanted_day = first_day + datetime.timedelta(delta)
            interval = wanted_day - first_day_of_year
            num = interval.days + 1
            out2.append(num)

    resultJson = {}
    logging.info("My result :{}".format(resultJson))
    resultJson["part1"] = out
    resultJson["part2"] = out2
    return json.dumps(resultJson)