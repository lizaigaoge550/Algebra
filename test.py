import copy
from opt_class import Project
from class_file import cClass
import nltk


class A:
    def __init__(self,param):
        self.param_list = [param]




class B:
    def __init__(self,name,val):
        self.name = name
        self.val = val

c = cClass(t_name='carsale', c_name='sale', c_type='number', value='carsale.sale')
a = Project(None,None,None)
a.param_1 = c

b = copy.deepcopy(a)
b.param_1.description = 'carsale.salebbbb'

print(a.param_1.description)
print(b.param_1.description)

s = 'string'

if 'string' in s:print(True)


s = "shark.count(*)"
s = s[:s.index('(')]
print(s)

print(type(c).__name__.lower())

s = 'F'
print(s.split('.'))

s = "？，。"
print(nltk.tokenize.word_tokenize(s))