import functools

@functools.lru_cache
def find_with_cost(index):
	'''
	it will cost a lot of time to locate an index
	'''
	print('run the function before return')
	return index
index=0
for i in range(10):
	#find_with_cost.cache_clear()
	find_with_cost(index)
	print(find_with_cost.cache_info())

