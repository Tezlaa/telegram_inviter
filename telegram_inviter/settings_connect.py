class SettingsConnect:
    API_ID: str
    API_HASH: str
    PHONE_NUMBER: str

    def __init__(
        self,
        API_ID,
        API_HASH,
        PHONE_NUMBER
    ):
        self.API_ID = API_ID
        self.API_HASH = API_HASH
        self.PHONE_NUMBER = PHONE_NUMBER

    def __str__(self):
        return f'Connect:{self.PHONE_NUMBER}'
