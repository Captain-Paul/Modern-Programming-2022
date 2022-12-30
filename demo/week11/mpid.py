from multiprocessing import Process

def run():
	while(1):
		pass

if __name__=='__main__':
	while(True):
		p=Process(target=run)
		p.start()
		print(f"{p.pid}")