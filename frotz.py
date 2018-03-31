from subprocess import Popen, PIPE
from Queue import Queue
from threading import Thread
from time import sleep

import os

from ConfigParser import ConfigParser

class DFrotz(object):
    """
    Simple interface to dfrotz
    """
    def __init__(self, path_to_dfrotz,
                       path_to_game,
                       path_to_backupfile):
        self.outputQ = Queue()
        self.process = Popen([path_to_dfrotz,
                              path_to_game],
                             stdin=PIPE,
                             stdout=PIPE)
        self.readoutputthread = Thread(target=self._fillQ,
                                       args=[self.process.stdout, self.outputQ])
        self.readoutputthread.daemon = True
        self.readoutputthread.start()
        self.backupfile = path_to_backupfile

    def _fillQ(self, output, Q):
        for line in iter(output.readline, ''):
            Q.put(line)
        output.close()

    def get_output(self):
        ret_string = ''
        while not self.outputQ.empty():
            line = self.outputQ.get()
            if not ('Score' in line and 'Moves' in line):
                ret_string += line
        return ret_string

    def do(self, command):
        """
        pipe command to frotz

        @param string command, to be send to frotz-process
            special commands: quit, save, restore
        @return bool terminate
        """
        if command == 'quit':
            # FIXME allow user to shut down the bot?
            self.process.stdin.write('quit\n')
            sleep(0.1)
            self.process.stdin.write('Y\n')
            sleep(0.1)
            self.readoutputthread.join()
            self.outputQ.queue.clear()
            self.outputQ.put('Ok, quitted.')
            return True
        elif command == 'save':
            self.process.stdin.write('save\n')
            sleep(0.1)
            self.process.stdin.write(self.backupfile + '\n')
            sleep(0.1)
            if os.path.exists(self.backupfile): # overwrite
                self.process.stdin.write('Y\n')
            sleep(0.1)
            self.outputQ.queue.clear()
            self.outputQ.put('Ok, saved.')
            return False
        elif command == 'restore':
            self.process.stdin.write('restore\n')
            sleep(0.1)
            self.process.stdin.write(self.backupfile + '\n')
            sleep(0.1)
            self.outputQ.queue.clear()
            self.outputQ.put('Ok, restored.')
            return False
        else:
            self.process.stdin.write(command + '\n')
            return False

if __name__ == '__main__':
    config = ConfigParser()
    config.read('tfbot.conf')

    ZM = DFrotz(config.get('frotz', 'path'),
                config.get('game', 'file'),
                config.get('game', 'backup'))

    sleep(0.2)
    print(ZM.get_output())

    terminated = False
    while not terminated:
        x = raw_input(">")
        terminated = ZM.do(x)
        sleep(0.1)
        print(ZM.get_output())
