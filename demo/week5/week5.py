class Future:
	def __init__(self,ret):
		self._ret=ret

class Stock(Future):
	ID=0
	def __init__(self, price, volume, ret):
		super().__init__(ret)
		self._price=price
		self.__volume=volume
		self.ID+=1

	def get_price(self):
		return self._price

	def set_price(self,price):
		self._price=price

	def get_volume(self):
		return self.__volume


def main():
	s=Stock(10.0,1000,1.0)
	print(Stock.__dict__)
	print(s._price)
	print(s._Stock__volume)
	print(s._ret)
	print(s.ID)


if __name__=='__main__':main()