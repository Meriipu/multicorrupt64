import collections
  
def setup():
  L = ['sleep 1',
       'keydown f',
       #'sleep 15',
       'key Return',
       'sleep 2',
       'key Return',
       'sleep 30',
       'keyup f',
       'sleep 2'
       ]
  for step in L: 
    yield step
  yield A()
  yield 'sleep 1'
  yield A()
  yield 'sleep 1'
  
def A():
    yield 'key Shift_L'
def Z():
    yield 'key Z'
def B():
    yield 'key Control_L'

def I(t):
    yield 'keydown Up'
    yield 'sleep {}'.format(t)
    yield 'keyup Up'
def J(t):
    yield 'keydown Left'
    yield 'sleep {}'.format(t)
    yield 'keyup Left'
def K(t):
    yield 'keydown Down'
    yield 'sleep {}'.format(t)
    yield 'keyup Down'
def L(t):
    yield 'keydown Right'
    yield 'sleep {}'.format(t)
    yield 'keyup Right'

def jump(t=0.2):
    yield 'keydown Shift_L'
    yield 'sleep {}'.format(t),
    yield 'keyup Shift_L'
def stomp():
  yield jump()
  yield Z()

def to_castle():
  #yield 'keydown f'
  yield stomp()
  yield 'sleep 1.5'
  yield L(0.6)
  yield 'sleep 0.2'
  yield J(0.6)
  yield 'sleep 0.2'
  yield 'keydown Up'
  yield 'sleep 0.2'
  for i in range(12):
    yield jump(0.1)
    yield 'sleep 0.1'
  
  yield 'sleep 1'
  yield 'keyup Up'
  yield 'keydown Down'
  yield 'sleep 0.5'
  yield jump()
  yield 'sleep 0.5'
  yield 'keyup Down'
  yield 'sleep 2'
  yield L(0.5)
  yield 'sleep 1'
  yield jump()
  yield 'sleep 2'
  yield I(2)
  yield 'sleep 2'
  yield I(0.2)
  yield 'sleep 2'
  yield jump()
  yield 'sleep 3'
  
  
  yield J(0.5)
  yield 'sleep 3'
  yield I(3)
  yield 'sleep 6'
  for i in range(8):
    yield A()
    yield 'sleep 0.5'
  yield 'sleep 1'
  
  yield 'keydown Z'
  yield I(4)
  yield 'keyup Z'
  
  yield 'sleep 1'
  for i in range(3):
    yield B()
    yield 'sleep 0.2'
  
  yield 'sleep 1'
  yield 'keydown Z'
  yield 'sleep 0.1'
  yield A()
  yield 'sleep 0.1'
  yield 'keyup Z'
  
  yield I(4)
  
  yield 'sleep 4'
  for i in range(3):
    yield A()
    yield 'sleep 0.5'

def to_bobomb():
  yield K(2)
  yield 'sleep 0.5'
  yield I(4)
  yield 'sleep 0.5'
  yield L(1)
  yield 'sleep 0.5'
  yield I(1)
  yield 'sleep 4'
  yield J(0.2)
  yield 'sleep 0.5'
  yield I(0.2)
  yield 'sleep 0.5'
  yield L(0.2)
  yield 'sleep 0.5'
  yield I(1)
  yield 'sleep 0.5'
  yield L(0.2)
  
  yield 'keydown Up'
  yield 'sleep 1.3'
  yield jump()
  yield 'keyup Up'
  
  yield 'sleep 5'
  yield 'key Return'
  yield 'sleep 4'
  for i in range(10):
    yield A()
    yield 'sleep 0.25'
def play():
  yield setup()
  yield to_castle()
  yield to_bobomb()


def unpack(gen):
  #base case
  if type(gen) == str:
    yield gen
  #can be unpacked more
  else:
    for elem in gen:
      yield from unpack(elem)
    
def main():
  yield from unpack(play())
    
  