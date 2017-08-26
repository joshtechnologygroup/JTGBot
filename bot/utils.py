import datetime
import hashlib
import json
import os
import re
import string

import apiai
import gspread
from django.conf import settings
from oauth2client.service_account import ServiceAccountCredentials

from bot.constants import LEAVES_TYPE_INDEX


def call_bot_api(query, email, json_key='query'):
    ai = apiai.ApiAI(settings.CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'
    request.session_id = get_session_id_of_user(email)
    setattr(request, json_key, query)
    response = request.getresponse()
    return json.loads(response.read())

def call_bot_event_api(email, event):
    ai = apiai.ApiAI(settings.CLIENT_ACCESS_TOKEN)
    request = ai.event_request(apiai.events.Event(event))
    request.lang = 'en'
    request.session_id = get_session_id_of_user(email)
    return request.getresponse()

def get_sheet_by_id(sheet_id):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(settings.BASE_DIR, 'bot/client_secret.json'), scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(sheet_id)


def get_contact_info_by_name(name, email, response_text=''):
    contact_sheet = get_sheet_by_id("1QHPyjulCMQD9K5wqHHth1mTs1lm-LcDcuIwX_UIGlas").worksheet('Contacts')
    header_row = contact_sheet.row_values(1)
    email_column = header_row.index('Josh ID')
    number_column = header_row.index('Cell Phone')
    cells = contact_sheet.findall(re.compile(r'(Small|{})'.format(name)))
    if len(cells) == 1:
        response = string.replace(response_text, 'phone', contact_sheet.row_values(cells[0].row)[number_column])
        response = string.replace(response, 'name', name)
    elif len(cells) == 0:
        response = call_bot_event_api(email, 'contact_regret')
        response = json.loads(response.read())['result']['fulfillment']['speech']
    else:
        result = 'Its seems like too many people share that name. Still, I tried.'
        for cell in cells:
            row = contact_sheet.row_values(cell.row)
            result = '{result} {number}({email})'.format(result=result, number=row[number_column], email=row[email_column])
        response = result
    return response


def get_official_leaves(vacation_type='', date_period=''):
    # todo get info from sheet
    return '2017-01-01', '2017-02-01', '2017-03-01', '2017-04-01','2017-05-01', '2017-06-01', '2017-07-01'


def get_session_id_of_user(email):
    return hashlib.md5(email).hexdigest()


def get_remaining_leaves_of_user(identity, vacation_type, response_text):
    dashboard_leaves_sheet = get_sheet_by_id("10rG0t-XhOSzGbbqls18gTlnksavBQTKxxdT8e1MZJn8").worksheet('Dashboard - Leaves')
    header_row = dashboard_leaves_sheet.row_values(1)
    cells = dashboard_leaves_sheet.findall(re.compile(r'(Small|{})'.format(identity)))
    leave_column = header_row.index('Leave Balance' if vacation_type == "CL" else "RH Availed (Jan '17 till Dec '17")
    email_column = header_row.index('Email')
    if len(cells) == 1:
        response = string.replace(response_text, 'vacation_type', vacation_type)
        response = string.replace(response, 'count', dashboard_leaves_sheet.row_values(cells[0].row)[leave_column])
    elif len(cells) == 0:
        response = "It's seems like, {} doesn't belong to our organisation".format(identity)
    else:
        result = "It's seems like too many people share that name. Still, I tried."
        for cell in cells:
            row = dashboard_leaves_sheet.row_values(cell.row)
            result = '{result} {email}({count})'.format(result=result, count=row[leave_column], email=row[email_column])
        response = result
    return response


def get_team_status(team_name, date):
    vacation = get_sheet_by_id("10rG0t-XhOSzGbbqls18gTlnksavBQTKxxdT8e1MZJn8").worksheet(
        'Vacation Tracker'
    )
    column_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    requested_date = int(column_date.strftime('%d'))
    column_name = column_date.strftime('%B - %Y')
    header_row = vacation.row_values(1)
    column_index = header_row.index(column_name)
    name_index = header_row.index('Name')
    cells = vacation.findall(re.compile(r'(Small|{})'.format(team_name)))
    result = ''
    for cell in cells:
        row = vacation.row_values(cell.row)
        for i in range(0, 5):
            dates = [date_string.split('(')[0].strip() for date_string in row[column_index + i].split(',')]
            if requested_date in [int(date) for date in dates if date.isdigit()]:
                result = '{result} {name} {vaction_type}, '.format(
                    result=result, name=row[name_index], vaction_type=vacation.row_values(2)[column_index + i]
                )
                break
    if result:
        if column_date.date() > datetime.date.today():
            helping_verb = 'wil be'
        else:
            helping_verb = 'is'
        result = string.replace(result, 'Leaves', '{} on leave'.format(helping_verb))
        result = string.replace(result, 'WFH', '{} working from home'.format(helping_verb))
        result = string.replace(result, 'RH', '{} on leave'.format(helping_verb))
        result = string.replace(result, 'Half Days', '{} on half day'.format(helping_verb))
    elif len(cells) == 0:
        result = "It's seems like, {} team doesn't belongs to our organisation".format(team_name)
    else:
        result = 'Good news for you, everyone is available'
    return result


def apply_vacation(email, data_list, vacation_type):
    vacation_sheet = get_sheet_by_id("10rG0t-XhOSzGbbqls18gTlnksavBQTKxxdT8e1MZJn8").worksheet(
        'Applied Tracker'
    )
    header_row = vacation_sheet.row_values(1)
    user_row = vacation_sheet.find(re.compile(r'(Small|{})'.format(email))).row
    applied_leaves_data = {}

    for data in data_list:
        date = data.get('date')
        date_period = data.get('date-period')
        if date:
            column_index, requested_day = process_vacation_date(date, vacation_type, header_row)
            applied_leaves_data.setdefault(column_index, []).append(requested_day)
        if date_period:
            for date in date_period.split('/'):
                column_index, requested_day = process_vacation_date(date, vacation_type, header_row)
                applied_leaves_data.setdefault(column_index, []).append(requested_day)
    cells_list = []
    for vacation_column, leaves_list in applied_leaves_data.items():
        cell = vacation_sheet.cell(user_row, vacation_column)
        cell.value = ','.join(str(day) for day in set(cell.value.split(',') + leaves_list))
        cells_list.append(cell)
    vacation_sheet.update_cells(cells_list)
    return 'Done'


def process_vacation_date(date, vacation_type, header_row):
    requested_date_object = datetime.datetime.strptime(date, '%Y-%m-%d')
    requested_day = requested_date_object.strftime('%d')
    column_name = requested_date_object.strftime('%B - %Y')
    column_index = header_row.index(column_name) + LEAVES_TYPE_INDEX.get(vacation_type, 0) + 1
    return column_index, requested_day