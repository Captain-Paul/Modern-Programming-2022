from threading import Thread,Lock
import time
import signal
import sys

counter=0

class Task(Thread):
	def __init__(self,name,lock):
		super().__init__()
		self._name=name
		self._lock=lock

	def run(self):
		while(True):
			time.sleep(1)
			with self._lock:
				global counter
				counter+=1


def handler(signum,frame):
	global counter
	print(f'counter={counter}')
	

def main():
	signal.signal(signal.SIGINT,handler)
	#signal.signal(signal.SIGALRM,handler)
	lock=Lock()
	for i in range(0,100):
		t=Task(f'thread-{i}',lock)
		t.start()
	signal.alarm(10)

if __name__=='__main__':
	main()

'''
在Windows下，signal模块可能存在一定限制，无法使用SIGALRM信号。

只能使用:

SIGABRT
SIGFPE
SIGILL
SIGINT
SIGSEGV
SIGTERM
'''