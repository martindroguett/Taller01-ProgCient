import sys
import time
import threading
import itertools

class Spinner:
    """
    Clase auxiliar que muestra una animación de carga por consola cuando se inicializa.

    Attributes:
        msg (str): Mensaje que muestra en consola y acompaña la animación.
        stopped (boolean): Índica si la animación está activa o no.
        thread (Thread): Hilo encargado de la animación.
    """

    def __init__(self, msg="Cargando"):
        self.msg = msg
        self.stopped = False
        self.thread = None

        self.start()

    def start(self):
        """
        Función que activa la animación del spinner.
        """
        self.stopped = False
        self.thread = threading.Thread(target=self.__animate)
        self.thread.start()

    def change_text(self, msg="Cargando"):
        """
        Cambia el texto mostrado por consola sin dejar de ejecutarse.

        Args:
            msg (str): Mensaje nuevo.
        """

        self.msg = msg

    def __animate(self):
        """
        Se encarga de la definición de carácteres de la animación y de su ejecución por consola.
        """

        chars = itertools.cycle(['-', '\\', '|', '/'])
        while not self.stopped:
            sys.stdout.write(f'\r{self.msg} {next(chars)}')
            sys.stdout.flush()
            time.sleep(0.2)

        sys.stdout.write(f'\r{self.msg} Listo!\n')
        sys.stdout.flush()

    def stop(self):
        """
        Detiene la animación.
        """

        self.stopped = True
        if self.thread is not None:
            self.thread.join()