import os
import time
import sys
import pathlib
import glob
import tempfile
from faker import Faker
import linecache
import random

def path_join():
	paths=[
	('/','mnt','Volume'),
	('/Users','zjc','Downloads'),
	('~/Downloads','zhaojichang','Documents')
	]
	for path in paths:
		print('{!r}'.format(os.path.join(*path)))

def path_norm():
	paths=[
	'///mnt/Volume',
	'/Users//zjc/./Downloads',
	'~//Downloads/zhaojichang//Documents'
	]
	for path in paths:
		print('{!r}:{!r}'.format(path,os.path.normpath(path)))

def file_meta(path=__file__):
	print('File         :', path)
	print('Access time  :', time.ctime(os.path.getatime(path)))
	print('Modified time:', time.ctime(os.path.getmtime(path)))
	print('Change time  :', time.ctime(os.path.getctime(path)))
	print('Size         :', os.path.getsize(path)//1024,'K')

def file_info(file=__file__):
	p=pathlib.Path(file)
	stat_info=p.stat()
	print('{}:'.format(file))
	print('  Size:', stat_info.st_size)
	print('  Permissions:', oct(stat_info.st_mode))
	print('  Owner:', stat_info.st_uid)
	print('  Device:', stat_info.st_dev)
	print('  Created      :', time.ctime(stat_info.st_ctime))
	print('  Last modified:', time.ctime(stat_info.st_mtime))
	print('  Last accessed:', time.ctime(stat_info.st_atime))

def list_f(path='.',ext='*.py'):
	p=pathlib.Path(path)
	#for f in p.iterdir():
	#	print(f)
	for f in p.glob(ext):
		print(f)

def fake_f(file,maxn=1024*1024*1024):
	faker=Faker(locale='zh-CN')
	with open(file,'w') as w:
		for i in range(maxn):
			s=','.join([faker.name(),faker.address(),
				faker.email(),faker.phone_number(),faker.password()])
			#print(s)
			w.write(s+'\n')
	print("generate a random file")

def main():
	#path_join()
	#path_norm()
	#file_meta(path=sys.argv[1])
	#file_info(file=sys.argv[1])
	#list_f()
	fake_f('./test_F.txt',maxn=100)
if __name__=='__main__':main()