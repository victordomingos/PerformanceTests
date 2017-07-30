import queue
import threading
import requests
from bs4 import BeautifulSoup
from bleach import clean

from timeit import default_timer as timer
from pprint import pprint

print('\n================\n a iniciar\n================')
start = timer()


def verificar_estado(tracking_code):
    """ Verificar estado de objeto nos CTT
    Ex: verificar_estado("EA746000000PT")
    """
    ctt_url = "http://www.cttexpresso.pt/feapl_2/app/open/cttexpresso/objectSearch/objectSearch.jspx?lang=def&objects=" + tracking_code + "&showResults=true"
    estado = "- N/A -"
    try:
        html = requests.get(ctt_url,timeout=5).content
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('table')
        cells = table('td')
        estado = cells[4].renderContents()
        estado = clean(estado, tags=[], strip=True).strip()
        if estado == "":  # se valor do ult. estado estiver vazio, usar as celulas da tabela seguinte para ler estado
            estado = cells[9].renderContents()
            estado = clean(estado, tags=[], strip=True).strip()
    except Exception as e:
        print(e)
    return (tracking_code, estado)


class Consumer(threading.Thread):
    ''' Define cada thread
    '''
    def __init__(self, queue, estados_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.estados_queue = estados_queue
        
    def run(self):        
        while True:
            task = self.queue.get()
            self.do_task(task)
            
    def do_task(self, task):
        estado = verificar_estado(task)
        self.estados_queue.put(estado)
        self.queue.task_done()    


def producer(lista_objetos):
    ''' 
    Produz as threads e queues necessárias, distribui as tarefas e recolhe os dados resultantes.
    '''
    mqueue = queue.Queue()
    estados_queue = queue.Queue()
    
    # adiciona tarefas à queue de entrada 
    for objeto in lista_objetos:        
        mqueue.put(objeto)
        
    # cria 6 threads e passa as duas queues como argumentos 
    for i in range(6):        
        mythread = Consumer(mqueue, estados_queue)        
        mythread.daemon = True        
        mythread.start()
        
    # espera que termine a queue de entrada (lista de tarefas) 
    mqueue.join()
    return list(estados_queue.queue)


if __name__ == "__main__":
    lista_objetos = [ 'EA123456786PT', 'EA123456787PT', 'EA000000000PT', 'RC123456789PT']
    estados = producer(lista_objetos)
    end = timer()
    delta = end - start
    estatisticas = '================\nTempo de execução: ' + str(delta) + ' segundos.'
    pprint(estados)
    print(estatisticas)