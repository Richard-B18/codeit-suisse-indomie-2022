import datetime

import calendar
from calendar import Calendar
from codeitsuisse import app
import logging
import json

from flask import request

from codeitsuisse import app


def checkmonth(day, year):
    start = 1
    while day > 0 and start <= 12:
        day -= calendar.monthrange(year, start)[1]
        start += 1
    return start - 2


def checkdate(day, year):
    start = 1
    while day > 0 and start <= 12:

        days = calendar.monthrange(year, start)[1]
        if days < day:
            day -= days
        else:
            break
        start += 1
    return day - 1


def answer(numbers):
    start = datetime.date(numbers[0], 1, 1).weekday()

    total = 365 if numbers[0] % 4 != 0 else 366

    log = {}
    cal = Calendar()
    for i in range(0, 12):
        weeks = len(cal.monthdayscalendar(numbers[0], i + 1))
        log[i] = ['       '] * weeks

    for i in numbers[1:]:
        if i <= total and i > 0:
            date = (i - 1 + start) % 7
            check = log[checkmonth(i, numbers[0])]
            week_num = min((checkdate(i, numbers[0]) + start + 1) // 7, len(check) - 1)
            change = check[week_num]
            check = log[checkmonth(i, numbers[0])]
            log[checkmonth(i, numbers[0])][week_num] = change[:date] + 'mtwtfss'[date] + change[date + 1:]

    output = ''

    for i in log:
        ans = '       '
        count1, count2 = 0, 0
        for j in range(len(log[i])):
            count2 = max(count2, log[i][j].count('s'))
            for k in range(7):
                check = log[i][j][k]
                if check.isalpha() and ans[k] == ' ':
                    ans = ans[:k] + log[i][j][k] + ans[k + 1:]
                    if k < 5:
                        count1 += 1

        if count2 + count1 == 7:
            ans = 'alldays'
        elif count1:
            ans = 'weekday' if count1 == 5 else ans
        elif count2:
            ans = 'weekend' if count2 == 2 else ans

        output += ans + ','

    return output


def answer2(result):
    result = result.split(',')

    year = 2001 + result[0].find(' ')

    if year < 2001:
        return result
    ans = [year]
    days = 0
    start = datetime.date(year, 1, 1).weekday()

    for i in range(12):

        if result[i] == 'alldays':
            for j in range(7):
                ans.append(days + j + 1)

        elif result[i] == 'weekend':
            temp = datetime.date(year, i + 1, 1).weekday()

            day = 1

            while temp != 5:
                day += 1
                temp = (temp + 1) % 7
            ans += [days + day, days + day + 1]

        elif result[i] == 'weekday':
            temp = datetime.date(year, i + 1, 1).weekday()
            day = 1
            while temp != 0:
                day += 1
                temp = (temp + 1) % 7

            for j in range(5):
                ans.append(days + day + j)

        else:

            for j in range(1, 8):

                temp = (days + j + start) % 7

                if result[i][temp].isalpha():
                    ans.append(days + j + 1)

        days += calendar.monthrange(year, i + 1)[1]
    return ans


logger = logging.getLogger(__name__)


@app.route('/calendarDays', methods=['POST'])
def calendarDay():
    data = request.get_json()

    part1 = answer(data.get('numbers'))
    part2 = answer2(part1)

    response = dict(part1=part1, part2=part2)
    return json.dumps(response)