def foo(a, b):
  print(a, b)
  
def bar(a, b, test=None):
  print(a, b)
  print(test)
    
def spam(*args, **kwargs):
  print(args)
  print(kwargs)
    
def alot(a, b, *args, test=None, **kwargs):
  print(a, b)
  print(test)
  print(args)
  print(kwargs)
