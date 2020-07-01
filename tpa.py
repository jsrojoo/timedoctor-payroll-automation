import requests
from datetime import datetime, date, timedelta
import json
import csv
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
access_token = config['timedoctor']['access_token']

base_url = 'https://webapi.timedoctor.com/v1.1'
companies_api = 'companies'

def getTd(url, options={}):
    params = { **options, "access_token": access_token }
    url = f'{base_url}/{url}'
    return requests.get(url, params).json()

def getDecimal(h, m, s):
    seconds_hr = 3600
    min_hr = 60
    hours = int(h)
    mins = (int(m) / min_hr)
    secs = (int(s) / seconds_hr)
    return round(hours + mins + secs, 2)

def writeToCsv(logs):
    with open('worklog.csv', mode='w') as f:
        log_writer = csv.writer(
            f, delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )
        log_writer.writerow(['ID', 'DESCRIPTION', 'HOURS'])
        for i, log in enumerate(logs):
            (desc, hours) = log
            print(i + 1, desc, hours)
            log_writer.writerow([i + 1, desc, hours])

companies = getTd(companies_api, options={})
company_id = companies['user']['company_id']
work_logs_api = f'companies/{company_id}/worklogs'

prefix = 'Independent Contractor Services on'

logsToWrite = []

current_month_start = date.today().replace(day=1)
end_date = current_month_start - timedelta(days=1)
start_date = end_date.replace(day=1)
print('start_date', start_date)
print('end_date', end_date)
target_date = start_date

while target_date <= end_date:
    date_range = {
        "start_date": target_date,
        "end_date": target_date
    }
    logs = getTd(work_logs_api, date_range)
    total = logs['total']
    if total > 0:
        hour_str = str(timedelta(seconds=total))
        (h, m, s) = hour_str.split(':')
        work_hours_decimal = getDecimal(h, m, s)
        service_date = target_date.strftime('%B %-d, %Y')
        description = f'{prefix} {service_date}'
        logsToWrite.append((description, work_hours_decimal))
        # print(description, work_hours_decimal, hour_str)
    target_date = target_date + timedelta(days=1)
#
# print(logsToWrite)
writeToCsv(logsToWrite)
