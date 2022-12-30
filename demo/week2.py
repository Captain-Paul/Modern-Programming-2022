import string
import textwrap
import difflib
import collections
import random
import heapq
import bisect

values = {'price':'5.99','dis':'50'}
t1 = string.Template("""PRICE: $price$$\nDISCOUNT: $dis%""")
print(t1.substitute(values))

sample_text="""    The textwrap module can be used to format text \
for output in situations where pretty-printing is desired. \
It offers programmatic functionality similar to the paragraph \
wrapping or filling features found in many text editors."""
#print(sample_text)


wrap=textwrap.dedent(sample_text)
wrap=textwrap.fill(wrap,width=50)
wrap4=textwrap.fill(wrap,initial_indent='',subsequent_indent=' '*4,width=50)
wrap=textwrap.indent(wrap,'>')
wraps=textwrap.shorten(sample_text,30,placeholder='...')
print(wrap4)
print(wraps)

s1='abcde'
s2='abcdf'

d = difflib.Differ()
diff = d.compare(s1,s2)
print(' '.join(diff))

d1={'path':'/c/d/e','cmd':'clear','pwd':'$'}
d2={'root':'/','cmd':'cls','pwd':'#','prompt':'True'}
d=collections.ChainMap(d1,d2)
print(d['path'])
print(d['cmd'])
d['cmd']='update'
print(d1['cmd'])
print(d2['cmd'])

freq=collections.Counter(['a', 'b', 'c', 'a', 'a', 'b'])
freq.update('abca')
for l in 'abc':
	print("{}:{}".format(l,freq[l]))

def default_value():
	return -1
dc = collections.defaultdict(default_value, zjc='38')
print(dc['zjc'])
print(dc['lsy'])
dc['lsy']+=1
print(dc['lsy'])


Student = collections.namedtuple('Student','name credit hometown')
s1=Student(name='zjc',credit='65',hometown='gs')
print(s1)
print(s1.credit)
#s1.hometown='bj'
print(s1.hometown)

dl=[random.randint(0,1000) for i in range(1000)]
dl.sort()
#print(dl)

dls=sorted(dl,reverse=True)

dls=[]
for n in dl:
	heapq.heappush(dls,n)
#print(dls)

heapq.heapify(dl)


d1=[random.randint(0,1000) for i in range(100)]
d2=[random.randint(0,1000) for i in range(100)]
d1.sort()
d2.sort()
d=list(heapq.merge(d1,d2))
#print(d)
#print(dl)

nums=[random.random() for i in range(10)]
l=[]
for n in nums:
	position = bisect.bisect(l, n)
	print(position)
	bisect.insort(l,n)
print(l)
