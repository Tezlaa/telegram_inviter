from telethon import TelegramClient, functions, types
from telegram_inviter.settings_connect import SettingsConnect


class TelegramInviterClient:
    def __init__(self, settings: SettingsConnect):
        self.client = TelegramClient(
            str(settings),
            settings.API_ID,
            settings.API_HASH
        )
        self.client.start(phone=settings.PHONE_NUMBER)

    async def request_to_contact(
        self,
        phone_number: str,
        first_name: str,
        last_name: str = '.'
    ) -> tuple[str | types.User, bool]:
        """
        Return:
            tuple[str, bool]
            str - (OK status/error message)
            bool - error or not
        """
        try:
            result = await self.client(functions.contacts.ImportContactsRequest(
                contacts=[
                    types.InputPhoneContact(
                        client_id=0,
                        phone=phone_number,
                        first_name=first_name,
                        last_name=last_name
                    )
                ]
            ))
            user = result.users[0]
        except Exception as e:
            return str(e), True

        return user, False

    async def delete_request_to_contact(self, user_id: int) -> tuple[str, bool]:
        """
        Return:
            tuple[str, bool]
            str - (OK status/error message)
            bool - error or not
        """
        try:
            await self.client(functions.contacts.DeleteContactsRequest(
                id=[user_id]
            ))
        except Exception as e:
            return str(e), True

        return 'OK', False

    async def add_user_to_chat(self, chat_id: int, user: types.User) -> tuple[str, bool]:
        """
        Return:
            tuple[str, bool]
            str - (OK status/error message)
            bool - error or not
        """
        try:
            await self.client(functions.channels.InviteToChannelRequest(
                channel=chat_id,
                users=[user]
            ))
        except Exception as e:
            return str(e), True

        return 'OK', False
