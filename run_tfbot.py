#!/usr/bin/python

from frotz import *

import sys

import telepot as tp
from telepot.loop import MessageLoop

class TFbot(DFrotz):
    """
    Telegram Frotz Bot

    FIXME: telepot.loop's MessageLoop cannot be canceled at the moment,
        see https://github.com/nickoala/telepot/issues/259,
        and https://github.com/nickoala/telepot/pull/267
        this might appear in a later version...
    """
    def __init__(self, config):
        self._bot = tp.Bot(config.get('telegram', 'token'))
        self._receiver = config.get('telegram', 'receiver')

        super(TFbot, self).__init__(config.get('frotz', 'path'),
                                    config.get('game', 'file'),
                                    config.get('game', 'backup'))

        # FIXME
        # self._messageloop_task = None

    def start(self):
        sleep(0.5)
        first_msg = self.get_output()
        if first_msg != '':
            self._bot.sendMessage(self._receiver, first_msg)

        # FIXME
        #self._messageloop_task = MessageLoop(self._bot, self._handle).run_forever()
        MessageLoop(self._bot, self._handle).run_as_thread()

    def _handle(self, msg):
        msg_text = msg['text']
        # TODO: test other stuff!
        if msg_text.find('/') == 0:
            msg_text = msg_text[1:].lstrip()
            self.do(msg_text)
            sleep(0.1)
            return_msg = self.get_output()
            self._bot.sendMessage(self._receiver, return_msg)

            # FIXME allow user to shut down the bot?
            #if (msg_text == 'quit'):
            #    # FIXME
            #    #self._messageloop_task.cancel()
            #    sys.exit(0)

if __name__ == '__main__':
    config = ConfigParser()
    config.read('tfbot.conf')

    tfbot = TFbot(config)
    tfbot.start()

    # keep everything alive
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
