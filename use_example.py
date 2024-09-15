import os
import csv


from dotenv import load_dotenv

from telegram_inviter.settings_connect import SettingsConnect
from telegram_inviter.telegram import TelegramInviterClient

load_dotenv()


CONNECT_1 = SettingsConnect(
    API_ID=os.getenv('API_ID_1'),
    API_HASH=os.getenv('API_HASH_1'),
    PHONE_NUMBER=os.getenv('PHONE_NUMBER_1')
)
CONNECT_2 = SettingsConnect(
    API_ID=os.getenv('API_ID_2'),
    API_HASH=os.getenv('API_HASH_2'),
    PHONE_NUMBER=os.getenv('PHONE_NUMBER_2')
)

CHAT_ID_1 = int(os.getenv('CHAT_ID_1'))


def read_from_file(file_path: str) -> list[tuple[str, str]]:
    result = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, fieldnames=['phone_number', 'full_name'])
        for row in reader:
            result.append((row['phone_number'], row['full_name']))
    return result


async def main(client_1, client_2, contacts):
    error_contacts = []
    for phone_number, full_name in contacts:
        user, error = await client_1.request_to_contact(
            phone_number=phone_number,
            first_name=full_name
        )
        if error:
            error_contacts.append((phone_number, full_name))
            print(f'{phone_number} - {full_name} Error: {user}')
            continue

        # user, error = await client_2.request_to_contact(
        #     phone_number=phone_number,
        #     first_name=full_name
        # )
        # if error:
        #     error_contacts.append((phone_number, full_name))
        #     continue

        m, error = await client_1.add_user_to_chat(chat_id=CHAT_ID_1, user=user)
        if error:
            error_contacts.append((phone_number, full_name))
            print(f'{phone_number} - {full_name} Error: {m}')
            continue

        m, error = await client_1.delete_request_to_contact(user_id=user.id)
        if error:
            error_contacts.append((phone_number, full_name))
            print(f'{phone_number} - {full_name} Error: {m}')
            continue
        print(f'{phone_number} - {full_name} Added')

    print(error_contacts)


if __name__ == '__main__':
    client_1 = TelegramInviterClient(CONNECT_1)
    client_2 = None
    with client_1.client:
        client_1.client.loop.run_until_complete(main(client_1, client_2, read_from_file('contacts.csv')))
