from model import WordleDB
from multiprocessing import Process, Manager, Queue

__STOP_PROCESS__ = '__stop_process__'

db_process: Process = None
db_queue: Queue = None

def _process_queue(db_queue: Queue):
    wordle_db = WordleDB(readonly=False)
    db_fn_mapper = {
        'INSERT_WORD_INFO': wordle_db.insert_word_info
    }
    
    while True:
        msg = db_queue.get()
        req_type = msg[0]
        params = msg[1]

        if req_type == __STOP_PROCESS__:
            wordle_db.close()
            break

        db_fn_mapper[req_type](*params)

def start_process() -> Queue:
    global db_queue
    manager = Manager()
    db_queue = manager.Queue()

    global db_process
    db_process = Process(
        target=_process_queue,
        args=(db_queue, )
    )
    db_process.start()

    return db_queue

def stop_process():
    global db_queue
    db_queue.put((__STOP_PROCESS__, None))

    global db_process
    db_process.join()
    db_process.close()
