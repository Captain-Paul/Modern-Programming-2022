from threading import Thread, Lock

class Vector:
    def __init__(self):
        self._list = []
        self._lock = Lock()
    
    def get(self, index):
        if index >= 0 and index < len(self._list):
            return self._list[index]
        return None
    
    def add(self, value):
        with self._lock:
            self._list.append(value)
    
    def pop(self):
        if len(self._list) > 0:
            with self._lock:
                return self._list.pop()
        return None
    
    def len(self):
        return len(self._list)

class TestAdd(Thread):
    def __init__(self, vector, elements):
        super().__init__()
        self._vector = vector
        self._elements = elements
    
    def run(self):
        for element in self._elements:
            self._vector.add(element)
        
class TestLen(Thread):
    def __init__(self, vector):
        super().__init__()
        self._vector = vector
    
    def run(self):
        print(f'Length is {self._vector.len()}')

class TestGet(Thread):
    def __init__(self, vector, indices):
        super().__init__()
        self._vector = vector
        self._indices = indices
    
    def run(self):
        for index in self._indices:
            print(self._vector.get(index))

class TestPop(Thread):
    def __init__(self, vector, times):
        super().__init__()
        self._vector = vector
        self._times = times
    
    def run(self):
        for i in range(self._times):
            print(self._vector.pop())

if __name__ == '__main__':
    vec = Vector()
    test_add_1 = TestAdd(vec, [1, 2, 3])
    test_add_2 = TestAdd(vec, [4, 5, 6])
    test_add_3 = TestAdd(vec, [7, 8, 9])
    
    test_add_1.start()
    test_add_2.start()
    test_add_3.start()
    test_add_1.join()
    test_add_2.join()
    test_add_3.join()
    print(vec._list)