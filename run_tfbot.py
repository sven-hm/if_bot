#!/usr/local/bin/python2.7

from frotz import *

import sys

import telepot as tp
from telepot.loop import MessageLoop

from PyDictionary import PyDictionary

class TFbot(object):
    """
    Telegram Frotz Bot

    FIXME: telepot.loop's MessageLoop cannot be canceled at the moment,
        see https://github.com/nickoala/telepot/issues/259,
        and https://github.com/nickoala/telepot/pull/267
        this might appear in a later version...
    """
    def __init__(self, config):
        self._bot = tp.Bot(config.get('telegram', 'token'))

        self._frotz_instances = dict()

        # FIXME
        # self._messageloop_task = None

        self._dictionary = PyDictionary()

    def start(self):
        # FIXME
        #self._messageloop_task = MessageLoop(self._bot, self._handle).run_forever()
        MessageLoop(self._bot, self._handle).run_as_thread()

    def _handle(self, msg):
        msg_text = msg['text']
        rid = msg['chat']['id']
        #self._bot.sendMessage(rid, str(rid))

        if msg_text.find('/') == 0:
            msg_text = msg_text[1:].lstrip()
        if msg_text.find('?') == 0:
            msg_text = msg_text[1:].lstrip()
            if msg_text.find('?') == 0:
                # try to translate 
                try:
                    translation = self._dictionary.meaning(msg_text)
                except:
                    self._bot.sendMessage(rid, 'failed to search for translation :(')
                for t in translation:
                    self._bot.sendMessage(rid, t)
                return

            # try to get meaning
            try:
                meaning = self._dictionary.meaning(msg_text)
            except:
                self._bot.sendMessage(rid, 'failed to search for word meaning :(')
            if type(meaning) is dict:
                for word_type in meaning:
                    return_msg = word_type + ': '
                    for m in meaning[word_type]:
                        return_msg += m + '\n'
                    self._bot.sendMessage(rid, return_msg)
            else:
                self._bot.sendMessage(rid, 'failed to search for word meaning :(')
            return

        msg_parts = msg_text.split(' ')

        if len(msg_parts) == 2 and msg_parts[0] == 'start':
            if rid in self._frotz_instances.keys():
                self._bot.sendMessage(rid, 'quit old game first...')
                self._frotz_instances[rid].do('quit')
                del self._frotz_instances[rid]

            try:
                # create new
                self._frotz_instances[rid] = DFrotz(
                                        config.get('frotz', 'path'),
                                        config.get(msg_parts[1], 'file'),
                                        'backup_' + str(rid) + msg_parts[1] + '.qzl')
            except:
                self._bot.sendMessage(rid, 'failed to start game :(')
                return

            self._bot.sendMessage(rid, 'starting ' + msg_parts[1])
            sleep(1.0)
            first_msg = self._frotz_instances[rid].get_output()
            if first_msg != '':
                self._bot.sendMessage(rid, first_msg)

        else:
            if rid in self._frotz_instances.keys():
                #self._bot.sendMessage(rid, msg_text)
                if self._frotz_instances[rid].do(msg_text):
                    del self._frotz_instances[rid]
                    return
                sleep(0.1)
                return_msg = self._frotz_instances[rid].get_output()
                self._bot.sendMessage(rid, return_msg)
            else:
                self._bot.sendMessage(rid, '_no_ game running :(')

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
