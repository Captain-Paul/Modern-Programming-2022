class X:pass
class Y: pass
class A(X, Y):pass
class B(Y, X):pass
#class C(A, B):pass

print(A.__mro__)
print(B.__mro__)

#print(C.__mro__)