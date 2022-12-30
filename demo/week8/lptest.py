from line_profiler import LineProfiler
import random

def do_other_stuff(numbers):
    s = sum(numbers)

def do_stuff(numbers):
    do_other_stuff(numbers)
    l = [numbers[i]/43 for i in range(len(numbers))]
    m = ['hello'+str(numbers[i]) for i in range(len(numbers))]

numbers = [random.randint(1,100) for i in range(1000)]
lp = LineProfiler()
lp.add_function(do_other_stuff)   # add additional function to profile
lp_wrapper = lp(do_stuff)
lp_wrapper(numbers)
lp.print_stats()