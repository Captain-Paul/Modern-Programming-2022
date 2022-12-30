import abc

class Vbase(abc.ABC):

	@abc.abstractmethod
	def protocol_method_must(self):
		pass

	@classmethod
	def __subclasshook__(cls,subclass):
		print(f"__subclasshook__: cls={cls}, subclass={subclass}")
		if cls is Vbase:
			if any('protocol_method_must' in B.__dict__ for B in subclass.__mro__):  #mro查找父类
				return True
		return NotImplemented 

class Democlass:   #虚拟子类

	def protocol_method_must(self):
		pass

if __name__ == '__main__':
	demo=Democlass()
	#print(Vbase.__subclasses__())
	print(isinstance(demo,Vbase))
	#print(Vbase.__subclasses__())
	print(issubclass(Democlass,Vbase))
	#print(Vbase.__subclasses__())
	