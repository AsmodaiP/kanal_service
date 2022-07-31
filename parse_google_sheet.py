import datetime
import logging
import os
from re import S
from typing import List

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from tqdm import tqdm

from convert_valute import get_course
from database import SuppliesManager, Supply
from settiings import CURRENCY_CODE, CHAT_ID_FOR_NOTIFICATION
from bot import bot

load_dotenv()

VALUES_POSITION = {
    'number': 1,
    'price_in_valute': 2,
    'date': 3,
}


def parse_google_sheet(sheet_id: str, sheet_name: str, credentials: service_account.Credentials) -> List[List[str]]:
    """Parse rows  from google sheet."""
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=sheet_name).execute()
    values = result.get('values', [])
    return values


def get_credentials() -> service_account.Credentials:
    """Get credentials for google service account."""
    path_to_credentials = os.getenv('GOOGLE_SHEET_CREDENTIALS')
    scopes = ('https://www.googleapis.com/auth/spreadsheets.readonly',)
    credentials = service_account.Credentials.from_service_account_file(
        path_to_credentials, scopes=scopes)
    return credentials


def parse_row_to_supply(row: List[str], current_course: float) -> Supply:
    """Parse row to supply using positions from VALUES_POSITION."""
    order_number = int(row[VALUES_POSITION['number']])
    price_in_valute = int(row[VALUES_POSITION['price_in_valute']])
    date = datetime.datetime.strptime(row[VALUES_POSITION['date']], '%d.%m.%Y')
    price_in_rub = int(price_in_valute*current_course)
    return Supply(order_number=order_number,
                  price_in_valute=price_in_valute, price_in_rub=price_in_rub, date=date)


def update_supplies():
    """Update supplies from google sheet."""
    current_course = get_course(CURRENCY_CODE)
    supplies_manager = SuppliesManager()
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    sheet_name = os.getenv('GOOGLE_SHEET_NAME')
    credentials = get_credentials()
    values = parse_google_sheet(sheet_id, sheet_name, credentials)
    supplies = []
    for row in tqdm(values[1:]):
        try:
            supply = parse_row_to_supply(row, current_course)
            supplies.append(supply)
        except Exception as e:
            logging.error(e, exc_info=True)
    supplies_manager.delete_all_supplies()
    supplies_manager.add_multiple_supplies(supplies)
    logging.info(f'Supplies updated')
