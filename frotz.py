from subprocess import Popen, PIPE
from Queue import Queue
from threading import Thread
from time import sleep

from ConfigParser import ConfigParser

class DFrotz(object):
    """
    Simple interface to dfrotz
    """
    def __init__(self, path_to_dfrotz, path_to_game):
        self.outputQ = Queue()
        self.process = Popen([path_to_dfrotz,
                              path_to_game],
                             stdin=PIPE,
                             stdout=PIPE)
        self.readoutputthread = Thread(target=self._filloutQ,
                                       args=[self.process.stdout, self.outputQ])
        self.readoutputthread.daemon = True
        self.readoutputthread.start()

    def _filloutQ(self, output, Q):
        for line in iter(output.readline, ''):
            Q.put(line)
        output.close()

    def get_output(self):
        ret_string = ''
        while not self.outputQ.empty():
            line = self.outputQ.get()
            if not ('Score' in line and 'Moves' in line) and line != '\n':
                ret_string += line
        return ret_string + '\n'

    def do(self, command):
        #if command == 'quit':
        #    self.process.stdin.write('quit\n')
        #    sleep(0.1)
        #    self.process.stdin.write('Y\n')
        #    sleep(0.1)
        #    self.readoutputthread.join()
        #    return True
        #elif command == 'save':
        #    # FIXME: if file exists, asks if to overwrite
        #    self.process.stdin.write('save\n')
        #    sleep(0.1)
        #    self.process.stdin.write('\n')
        #    sleep(0.1)
        #    return False
        #elif command == 'restore':
        #    self.process.stdin.write('restore\n')
        #    sleep(0.1)
        #    self.process.stdin.write('\n')
        #    pass
        #else:
        self.process.stdin.write(command + '\n')
        return False

if __name__ == '__main__':
    config = ConfigParser()
    config.read('tfbot.conf')

    ZM = DFrotz(config.get('frotz', 'path'), config.get('game', 'path'))

    sleep(0.2)
    print(ZM.get_output())

    terminated = False
    while not terminated:
        x = raw_input(">")
        terminated = ZM.do(x)
        sleep(0.1)
        print(ZM.get_output())
