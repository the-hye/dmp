from multiprocessing import Queue
import time
from . import user 

queue = Queue(-1)

def fn_queue(queue):
    while(1):
        if queue.empty() == False:
            s = queue.get()
            url = s.get('url')
            # print(s)
            data = s.get('data')
            if 'insert' in url:
                user.user_insert(data)
                print('insert at fn_queue') 

            elif 'update' in url:
                user.user_update(data)
                print('update at fn_queue') 

            elif 'state' in url:
                user.user_state(data)
                print('update state at fn_queue') 

            elif 'delete' in url:
                user.user_delete(data)
                print('delete at fn_queue') 
              
        else:
            print('22')
            time.sleep(10)