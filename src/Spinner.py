import sys
import time
import threading
import itertools

class Spinner:
    def __init__(self, msg="Cargando"):
        self.msg = msg
        self.stopped = False
        self.thread = None

    def start(self):
        self.stopped = False
        self.thread = threading.Thread(target=self.__animate)
        self.thread.start()

    def __animate(self):
        chars = itertools.cycle(['-', '\\', '|', '/'])
        while not self.stopped:
            sys.stdout.write(f'\r{self.msg} {next(chars)}')
            sys.stdout.flush()
            time.sleep(0.3)

        sys.stdout.write(f'\r{self.msg} Listo!\n')
        sys.stdout.flush()

    def stop(self):
        self.stopped = True
        if self.thread is not None:
            self.thread.join()