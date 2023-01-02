from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import GetHistoryRequest
from . import config
import json


class Telegram:
    cc = {
        'running': config.hcolors.OKGREEN,
        'error': config.hcolors.FAIL,
        'warning': config.hcolors.WARNING,
        'ready': config.hcolors.WARNING
    }
    def __init__(self, settings={}) -> None:
        self.parse_settings(settings)
        if self.status == 'ready':
            self.load()
    
    def get_channel_posts(self, channel_username, limit=10):
        channel_entity=self.client.get_entity(channel_username)
        print(json.dumps(channel_entity.__dict__, indent=4))
        posts = self.client(GetHistoryRequest(
            peer=channel_entity,
            limit=limit,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0))
        return posts

    def load(self):
        self.client = TelegramClient('session_name',
                            self.api_id,
                            self.api_hash)

        if self.start_immediately:
            self.client.start()
            if not self.client.is_user_authorized():
                try:
                    print(config.hcolors.WARNING+"\t- Telegram client not actively authorized")
                    self.client.send_code_request(self.phone_number)
                    me = self.client.sign_in(self.phone_number, input(config.hcolors.BOLD+'\t\t- Enter code: '))
                except:
                    print(config.hcolors.FAIL+"\t- Telegram code sign in failed!")
                    self.status = 'error'
                    return
            
            self.status = 'running'
            

    def parse_settings(self, settings):
        if settings != None:
            _targets = ['api_id', 'api_hash', 'phone_number', 'start_immediately']
            for _target in _targets:
                if settings.get(_target) == None:
                    print(config.hcolors.FAIL+"\t- Telegram settings not configured correctly")
                    self.status = 'error'
                    return
                else:
                    setattr(self, _target, settings.get(_target))
            print(config.hcolors.OKBLUE+"\t- Telegram settings initialized")
            self.status = "ready"
            self.settings_dict = settings
            return

        print(config.hcolors.FAIL+"\t- Telegram settings not found")
        self.status = 'error'

    def print_status(self):
        print('\t- Telegram status: '+self.cc[self.status]+self.status)