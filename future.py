
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import time
def wait_on_b():
    print "A"
    return 5

def wait_on_a():
    time.sleep(1)
    print "B"
    return 6
executor = ThreadPoolExecutor(max_workers=2)
a = executor.submit(wait_on_b)
b = executor.submit(wait_on_a)


print a.done()
print b.done()

time.sleep(20)
