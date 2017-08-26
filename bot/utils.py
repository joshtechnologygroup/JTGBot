import json
import os
import re
import datetime

import apiai
import httplib2
import hashlib

# Create your views here.
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from apiclient import discovery

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def call_bot_api(query, email, json_key='query'):
    """
    :param query:
    :param email:
    :return:
    """
    ai = apiai.ApiAI(settings.CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'
    request.session_id = get_session_id_of_user(email)
    setattr(request, json_key, query)
    response = request.getresponse()
    return json.loads(response.read())


def get_sheet_by_id(sheet_id):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(settings.BASE_DIR, 'bot/client_secret.json'), scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(sheet_id)


def get_contact_info_by_name(name):
    contact_sheet = get_sheet_by_id("1QHPyjulCMQD9K5wqHHth1mTs1lm-LcDcuIwX_UIGlas").worksheet('Contacts')
    header_row = contact_sheet.row_values(1)
    email_column = header_row.index('Josh ID')
    number_column = header_row.index('Cell Phone')
    cells = contact_sheet.findall(re.compile(r'(Small|{})'.format(name)))
    result = {}
    for cell in cells:
        row = contact_sheet.row_values(cell.row)
        result.update({row[email_column]: row[number_column]})
    return result


def get_official_leaves(vaction_type='', date_period=''):
    # todo get info from sheet
    return ['2017-01-01', '2017-02-01', '2017-03-01', '2017-04-01','2017-05-01', '2017-06-01', '2017-07-01']


def get_session_id_of_user(email):
    return hashlib.md5(email).hexdigest()


def get_remaining_leaves_for_user(identity, vaction_type):
    dashboard_leaves_sheet = get_sheet_by_id("10rG0t-XhOSzGbbqls18gTlnksavBQTKxxdT8e1MZJn8").worksheet('Dashboard - Leaves')
    header_row = dashboard_leaves_sheet.row_values(1)
    cells = dashboard_leaves_sheet.findall(re.compile(r'(Small|{})'.format(identity)))
    leave_column = header_row.index('Leave Balance' if vaction_type == "CL" else "RH Availed (Jan '17 till Dec '17")
    email_column = header_row.index('Email')
    result = {}
    for cell in cells:
        row = dashboard_leaves_sheet.row_values(cell.row)
        result.update({row[email_column]: row[leave_column]})
    return result


def get_team_status(team_name, date):
    print get_sheet_by_id("10rG0t-XhOSzGbbqls18gTlnksavBQTKxxdT8e1MZJn8")
    vaction_sheet = get_sheet_by_id("10rG0t-XhOSzGbbqls18gTlnksavBQTKxxdT8e1MZJn8").worksheet(
        'Vacation Tracker'
    )
    column_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    column_name = column_date.strftime('%B - %Y')
    header_row = vaction_sheet.row_values(1)
    column_index = header_row.index(column_name)
    # print leaves_sheet.row_values(2)[52]
    cells = vaction_sheet.findall(re.compile(r'(Small|{})'.format(team_name)))
    result = []
    for cell in cells:
        row = vaction_sheet.row_values(cell.row)
        for i in range(0, 5):
            for string in row[column_index + 1].split(','):
                dates = string.split('(')[0].strip()
                if date in [int(date) for date in dates if date.isdigit()]:
                    result.append(date)
                    break
    return result
