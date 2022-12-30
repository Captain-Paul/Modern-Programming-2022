import pysnooper

@pysnooper.snoop()
def sum():
    s=0
    l=list(range(10))
    for i in l:
        s+=i
    return s

sum()