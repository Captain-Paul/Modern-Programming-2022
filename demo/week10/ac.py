import abc

class Fruit(metaclass=abc.ABCMeta):#class Fruit(abc.ABC)  
									#通过元类约定为抽象类(不能被实例化)
	@abc.abstractmethod  #抽象方法(必须被子类覆盖)
	def harvest(self):
		pass

	@abc.abstractmethod
	def grow(self):
		pass

#继承抽象类
class Apple(Fruit):
	
	def harvest(self):
		pass

	def grow(self):
		print("种苹果树")

	def juice(self):
		print("做苹果汁")

class Watermelon(Fruit):
	def harvest(self):
		#super().harvest()
		print("从地里摘")

	def grow(self):
		print("用种子种")

@Fruit.register  #注册抽象类
class Orange:
	def harvest(self):
		print("从树上摘")
	
	def grow(self):
		print("种橘子树")

#共同点: 需要实现抽象类方法; 都认为是子类
#不同点: 注册子类不保存在基类的子类列表中

#f=Fruit()
a=Apple()
a.grow()
w=Watermelon()
w.harvest()

o=Orange()
o.grow()

print(isinstance(o,Fruit))
print(issubclass(Orange,Fruit))
print([sc.__name__ for sc in Fruit.__subclasses__()]) #no orange

