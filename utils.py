from opt_class import *
def add(a, l):
    if type(a) == list:
        for i in range(len(a)):
            if a[i] not in l: l.append(a[i])
    else:
        if a != None and a not in l: l.append(a)
    return l


def union(a, b):
    l = []
    # 检查类型
    l = add(a, l)
    l = add(b, l)
    if len(l) == 1: return l[0]
    if l == []: return None
    return l


def extract_option(v):
    opt = ""
    for i in range(len(v)):
        if v[i] != '(':
            opt += v[i]
        else:
            break
    return opt

def get_opt(value):
    if value == 'Project':
        return Project(None,None,None)
    elif value == 'Select':
        return Select(None,None,None)
    elif value == 'group':
        return Group(None,None,None)
    elif value == 'min':
        return Min(None,None,None)
    elif value == 'max':
        return Max(None,None,None)
    elif value == 'avg':
        return Avg(None,None,None)
    elif value == 'sum':
        return Sum(None,None,None)
    elif value == 'count':
        return Count(None,None,None)
    elif value == 'In':
        return In(None,None,None)
    elif value == 'And':
        return And(None,None,None)
    elif value == 'Or':
        return Or(None,None, None)
    elif value == 'Not':
        return Not(None,None,None)
    elif value == 'argmax':
        return Argmax(None,None,None)
    elif value == 'argmin':
        return Argmin(None,None,None)
    elif value == 'combine':
        return Combine(None,None,None)
    elif value == 'modify':
        return Modify(None,None,None)
    elif value == 'combineF':
        return CombineF(None,None,None)
    elif value == 'order':
        return Order(None,None,None)
    else:return None

#def extract_aggregate_value()