import threading
import time
import logging

from timeit import default_timer as timer


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def daemon():
    logging.debug('A contactar o servidor')
    time.sleep(5)
    logging.debug('A sair')


def non_daemon():
    logging.debug('A contactar o servidor')
    time.sleep(5)
    logging.debug('A Sair')


start = timer()
lista_daemon = []
lista_simples = []
USE_DAEMON = True

for i in range(10):
    if USE_DAEMON:
        logging.debug('Using daemon threads this time')
        d = threading.Thread(name='daemon', target=daemon)
        d.setDaemon(True)
        lista_daemon.append(d)
        d.start()
    else:
        logging.debug('Using regular non-daemon threads this time')
        t = threading.Thread(name='non-daemon', target=non_daemon)
        lista_simples.append(t)
        t.start()
    

logging.debug("Está tudo em processamento")

if USE_DAEMON:
    for i in lista_daemon:
        d.join()
else:
    for i in lista_simples:
        t.join()
    
if (threading.active_count()==1):
    logging.debug("acabou a festa !----------")
else:
    estado_app = 'threads ainda em curso: ' + str(threading.active_count())
    logging.debug(estado_app)

end = timer()
delta = end - start
estatisticas = 'Tempo de execução: ' + str(delta) + ' segundos.'
logging.debug(estatisticas)