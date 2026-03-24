import requests
import hashlib

from app.models import Ticket as TicketModel
from app.notification.base import BaseClass


class Mattermost(BaseClass):
    SERVER = str
    TOKEN = str
    CHANNEL_ID = str

    def __init__(self, server: str, token: str, channel_id: int):
        self.SERVER = server
        self.TOKEN = token
        self.CHANNEL_ID = channel_id

    def notify(self, ticket: TicketModel) -> None:
        data = {
            'channel_id': self.CHANNEL_ID,
            'props': {
                'override_username': 'ticket_alert',
                'attachments': [
                    {
                        'color': self.string_to_color(
                            f'{ticket.system_name}/{ticket.group}'
                        ),
                        'author_name': f'{ticket.system_name}/{ticket.group}',
                        'fallback': f'🎫 {ticket.system_name}/{ticket.group}\n{ticket.subject}',
                        'title': ticket.subject,
                        'title_link': ticket.url,
                        'fields': [],
                    }
                ],
            },
        }
        requests.post(
            f'https://{self.SERVER}/api/v4/posts',
            headers={'Authorization': f'Bearer {self.TOKEN}'},
            json=data,
        )

    def string_to_color(self, text: str) -> str:
        hash_object = hashlib.md5(text.encode('utf-8'))
        hash_hex = hash_object.hexdigest()

        color_hex = f'#{hash_hex[:6]}'

        return color_hex
