#coding=utf-8
from node import Node
from utils import get_opt
from opt_class import *
from class_file import cClass

import re


def fill_in_slot(opt,param,prefix):
    # c --> F F:count(c) c string, F:sum(c) c number
    # V --> Filter:In(c=V.c,V)
    # T --> F F:count(T)
    # D --> Filter:In(c=D.c,V)
    if type(opt) == Sum: #一个参数
        if param.c_type == 'number': #sum操作
            opt.param.val = param
            opt.c_name = param.c_name
            opt.t_name = param.t_name
            opt.c_type = param.c_type
        else:
            return None

    elif type(opt) == Count:
        if param.value == 'T':  #如果是T参数随意
            opt.param.val = param
            opt.c_name = 'count(t)'
            opt.t_name = param.t_name
            opt.c_type = 'number'

        # elif param.c_type == 'string': #count 操作
        #     opt.param.val = param
        #     opt.c_name = param.c_name
        #     opt.t_name = param.t_name
        #     opt.c_type = 'number'
        else:
            opt.param.val = param
            opt.c_name = param.c_name
            opt.t_name = param.t_name
            opt.c_type = 'number'

    elif type(opt) == In:
        # 第一个参数是c
        c = cClass(param.t_name, param.c_name, param.c_type, param.t_name + '.' + param.c_name)
        opt.param_1.val = c
        opt.param_2.val = param
        opt.t_name = param.t_name
        opt.c_name = param.c_name
        opt.c_type = param.c_type
        #opt.value = prefix
    opt.value = prefix
    return opt


# c --> F F:count(c) c string, F:sum(c) c number
def createVal(gnode, optype, child, prefix=""):
    opt = extract_opt(optype)
    cls = get_opt(opt) #count or select
    if cls == None:
        raise("Error OPtion {0}".format(opt))

    cls = fill_in_slot(cls,child.val,prefix)

    return cls


def extract_opt(opt):
    if '(' not in opt:
        return ""
    #去除括号
    new_opt = ''
    for i in range(len(opt)):
        if opt[i] != '(':
            new_opt += opt[i]
        else:
            return new_opt

def extract_paramter(func):
    if '(' not in func:return None
    arg = re.search('\(.*\)', func).group()[1:-1].split(',')
    return arg

def format_(l):
    args = [extract_paramter(i) for i in l.split('.')]
    a = []
    for i in range(len(args)):
        if args[i] != None: a.extend(args[i])

    if len(a) == 1: return a[0]
    else:return ",".join(a)

# c --> F F:count(c) c string, F:sum(c) c number
# V --> Filter:In(c=V.c,V)
# T --> F F:count(T)
# D --> Filter:In(c=D.c,D)
def type_rasing(gDict, nodelist, start, end, key=""):
    values = []
    for node in nodelist:
        values.append(node.val.value)
    for value in values:
        #有lambda 和 没有lambda
        if value == None:
            print(key)
            exit(100)
        if 'lambda' not in value: #(c-- > F=count(c))
            for rhs, lhs, func in gDict:
                if rhs == value and lhs not in values:
                    index = values.index(rhs)
                    option = createVal(lhs, func, nodelist[index], lhs)
                    if option == None: continue
                    values.append(lhs)
                    node = Node(nodelist[index], None, option, start, end)
                    nodelist.append(node)
        else:
            continue
            # prefix, v = value.split('.') #lambda(c).T
            # for rhs, lhs, func in gDict:
            #     if rhs == v:
            #         l = prefix+'.'+lhs #lambda(c).T
            #         #提取参数
            #         l = 'lambda('+ format_(l) + ')'+'.'+lhs
            #         if l not in values:
            #             index = values.index(value)
            #             option = createVal(lhs,func,nodelist[index],l)
            #             if option == None:continue
            #             values.append(l)
            #             node = Node(nodelist[index], None, option)
            #             nodelist.append(node)
    return nodelist
