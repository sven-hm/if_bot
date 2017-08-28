from subprocess import Popen, PIPE
from Queue import Queue
from threading import Thread
from time import sleep

from ConfigParser import ConfigParser

class DFrotz(object):
    """
    Interface to dfrotz
    """
    def __init__(self, path_to_dfrotz, path_to_game):
        self.outputQ = Queue()
        self.process = Popen([path_to_dfrotz,
                              path_to_game],
                             stdin=PIPE,
                             stdout=PIPE)
        self.readoutputthread = Thread(target=self._fillQ,
                                       args=[self.process.stdout, self.outputQ])
        self.readoutputthread.daemon = True
        self.readoutputthread.start()

    def _fillQ(self, output, Q):
        for line in iter(output.readline, ''):
            Q.put(line)
        output.close()

    def get_output(self):
        sleep(0.1)
        ret_string = ''
        while not self.outputQ.empty():
            line = self.outputQ.get()
            if not ('Score' in line and 'Moves' in line) and line != '\n':
                ret_string += line
        return ret_string

    def do(self, command):
        if command == 'quit':
            self.process.stdin.write('quit\n')
            sleep(0.1)
            self.process.stdin.write('Y\n')
            return True
        self.process.stdin.write(command + '\n')
        return False

if __name__ == '__main__':
    config = ConfigParser()
    config.read('tfbot.conf')

    ZM = DFrotz(config.get('frotz', 'path'), config('game', 'path'))

    terminated = False
    while not terminated:
        print ZM.get_output()
        x = raw_input(">")
        terminated = ZM.do(x)
