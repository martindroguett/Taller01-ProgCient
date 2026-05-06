import sys
import time
import threading
import itertools

class Spinner:
    def __init__(self, mensaje="Cargando"):
        self.mensaje = mensaje
        self.detener = False
        self.hilo = None

    def start(self):
        self.detener = False
        self.hilo = threading.Thread(target=self._animar)
        self.hilo.start()

    def _animar(self):
        caracteres = itertools.cycle(['-', '\\', '|', '/'])
        while not self.detener:
            sys.stdout.write(f'\r{self.mensaje} {next(caracteres)}')
            sys.stdout.flush()
            time.sleep(0.3)

        sys.stdout.write(f'\r{self.mensaje} Listo!\n')
        sys.stdout.flush()

    def stop(self):
        self.detener = True
        if self.hilo is not None:
            self.hilo.join()