class People:
	"""
	人的类，定义人相关的一些基本信息如姓名，身高，年龄等。

	"""
	def __init__(self,name,height,age):
		self._name=name
		self._height=height
		self._age=age

	def get_name(self):
		return self._name

	def set_name(self,name):
		self._name=name

	def get_height(self):
		return self._height

	def set_height(self,height):
		self._height=height

	def get_age(self):
		return self._age

	def set_age(self,age):
		self._age=age

	def print_info(self):
		print('in People')
		print('Name:{},Age:{},Height:{}'.\
			format(self.get_name(),self.get_age(),self.get_height()))

	def __add__(self,other):
		return self.get_height()+other.get_height()

class Speaker:
	"""
	演讲家类
	"""
	def __init__(self,topic):
		self._topic=topic

	def get_topic(self):
		return self._topic

	def set_topic(self,topic):
		self._topic=topic

	def speak(self):
		print('in Speaker')
		print("speak topic is {}".format(self.get_topic()))

class Student(People,Speaker):
	"""
	学生类，继承人的类，同时添加一些新的属性，并覆盖方法
	
	"""
	def __init__(self,name,height,age,topic,ID,major):
		People.__init__(self,name,height,age)
		Speaker.__init__(self,topic)
		self._ID=ID
		self._major=major

	def get_ID(self):
		return self._ID

	def set_ID(self,ID):
		self._ID=ID

	def get_major(self):
		return self._major

	def set_major(self,major):
		self._major=major

	def print_info(self):
		print('ID:{}, Name:{}, Major:{}, Age:{}, Height:{}'.\
			format(self.get_ID(),self.get_name(),self.get_major(), self.get_age(),self.get_height()))

	def speak(self):
		# super(Student,self).print_info()
		# super(Student,self).speak()
		super().print_info()
		super().speak()

p1=People('t3',175,40)
s1=Student('t2',175,35,'python',33060828,'cs')
print(p1+s1)

#s1.print_info()
s1.speak()

People.print_info(s1)
