from collections.abc import Iterator

class IterOneDuck:

	def __init__(self,start=0):
		self._start=start

	def __iter__(self):
		return self

	def __next__(self):
		tmp=self._start
		self._start+=1
		return tmp


iduck=IterOneDuck()


'''for duck in iduck:
	print(duck)
	if duck>10:break'''

print(Iterator.__dict__)
print(IterOneDuck.__dict__)
print(10 in iduck)
print(issubclass(IterOneDuck,Iterator))
print(isinstance(iduck,Iterator))


