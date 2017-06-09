import threading
import time
import logging
import requests

from queue import Queue
from timeit import default_timer as timer
from bs4 import BeautifulSoup
from bleach import clean


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )



def verificar_estado(tracking_code):
    """ Verificar estado de objeto nos CTT
    Ex: verificar_estado("EA746000000PT")
    """
    ctt_url = "http://www.cttexpresso.pt/feapl_2/app/open/cttexpresso/objectSearch/objectSearch.jspx?lang=def&objects=" + tracking_code + "&showResults=true"
    estado = "- N/A -"
    try:
        html = requests.get(ctt_url).content
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('table')
        cells = table('td')
        estado = cells[4].renderContents()
        estado = clean(estado, tags=[], strip=True).strip()
        if estado == "":  # se valor do ult. estado estiver vazio, usar as celulas da tabela seguinte para ler estado
            estado = cells[9].renderContents()
            estado = clean(estado, tags=[], strip=True).strip()
    except Exception as e:
        logging.debug(e)   
    return (tracking_code, estado)


def daemon():
    #logging.debug('A contactar o servidor')
    estado = verificar_estado('EA136625519PT')
    logging.debug(estado)
    #logging.debug('A sair')


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
    elif USE_DAEMON == False:
        logging.debug('Using regular non-daemon threads this time')
        t = threading.Thread(name='non-daemon', target=non_daemon)
        lista_simples.append(t)
        t.start()
    else:
        daemon()
    

logging.debug("Está tudo em processamento")

if USE_DAEMON:
    for i in lista_daemon:
        d.join()
else:
    for i in lista_simples:
        t.join()

    
estado_app = 'threads ainda em curso: ' + str(threading.active_count())
logging.debug(estado_app)
        
while (threading.active_count() > 1):
    logging.debug('A aguardar por threads restantes.\n')
    
    
logging.debug("\nPronto, acabou a festa!   ----------\n")


end = timer()
delta = end - start
estatisticas = 'Tempo de execução: ' + str(delta) + ' segundos.'
logging.debug(estatisticas)



