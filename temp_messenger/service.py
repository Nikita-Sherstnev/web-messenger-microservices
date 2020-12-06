from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http
from .dependencies.redis import MessageStore

import json


class KonnichiwaService:
    name = 'konnichiwa_service'

    @rpc
    def konnichiwa(self):
        return 'Konnichiwa!'


class WebServer:
    name = 'web_server'
    konnichiwa_service = RpcProxy('konnichiwa_service')
    message_service = RpcProxy('message_service')

    @http('GET', '/')
    def home(self, request):
        return self.konnichiwa_service.konnichiwa()

    @http('POST', '/messages')
    def post_message(self, request):
        data_as_text = request.get_data(as_text=True)

        try:
            data = json.loads(data_as_text)
        except json.JSONDecodeError:
            return 400, 'JSON payload expected'

        try:
            message = data['message']
        except KeyError:
            return 400, 'No message given'

        self.message_service.save_message(message)

        return 204, ''


class MessageService:
    name = 'message_service'
    message_store = MessageStore()

    @rpc
    def get_message(self, message_id):
        return self.message_store.get_message(message_id)

    @rpc
    def save_message(self, message):
        message_id = self.message_store.save_message(message)
        return message_id

    @rpc
    def get_all_messages(self):
        messages = self.message_store.get_all_messages()
        return messages
