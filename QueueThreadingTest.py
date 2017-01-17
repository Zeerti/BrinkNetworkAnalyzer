#Threading
#Queue
import queue
import threading
from threading import Thread

#Basic FIFO (First in, First out)


def do_stuff(q):
	while True:
		print(q.get())
		q.task_done()

q = queue.Queue(maxsize=0)
num_threads = 10

for i in range(num_threads):
	worker = Thread(target=do_stuff, args=(q,))
	worker.setDaemon(True)
	worker.start()
print(threading.activeCount())
for x in range(100):
	q.put(x)

q.join()



"""
def worker():
	while True:
		item = q.get()
		do_work(item)
		q.task_done()

q = queue.Queue()
for i in range(num_worker_threads):
	t = Thread(target=worker)
	t.daemon = True
	t.start()

for item in source():
	q.put(item)

q.join() #block until all tasks are completed
"""