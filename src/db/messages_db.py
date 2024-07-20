import json
import logging
from datetime import datetime

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from env.environment import DB_URI

log = logging.getLogger()


class MessagesDb:
    def __init__(self):
        self.client = MongoClient(DB_URI, server_api=ServerApi('1'))
        self.db = self.client.book

    def insert_message(self, data):
        message_data = json.loads(data)
        message_data['date'] = datetime.now()

        result = self.db.messages.insert_one(message_data)
        log.info(f'Inserted data to db\n{message_data}\n{result}')