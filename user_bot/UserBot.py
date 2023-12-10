from aiogram import Bot


class UserBot(Bot):
    bot_client: Bot

    def __init__(self, token: str):
        self.bot_client = super().__init__(token)

    def send_user_message(self, chat_id: int, message: str):
        self.bot_client.send_message(chat_id=chat_id, text=message)