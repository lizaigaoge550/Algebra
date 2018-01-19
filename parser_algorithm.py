#coding=utf-8
import re
from node import Node
from opt_class import *
from class_file import CClass,TClass
from type_raising import type_rasing
from combine import composition
from utils import extract_option,union,get_opt
import copy


def get_arg_express(node):
    assert 'lambda' in node.value
    try:
        arg, express = node.value.split(".")
    except:
        print(node.value)
        exit(0)
    arg = re.search('\(.*\)', arg).group()[1:-1].split(',')
    return arg, express


def generate_new_arg(arg, exp):
    new_arg = []
    for i in range(len(arg)):
        if arg[i] != exp:
            new_arg.append(arg[i])
    return new_arg


def extract_paramter(func):
    if '(' not in func: return None
    arg = re.search('\(.*\)', func).group()[1:-1].split(',')
    return arg


# and extract_paramter(node_val.value) == param.value
def fill_arg(node_val, param):
    # project包含(G)会出现迭代的情况, select包含(Filter)会出现迭代的情况, group(包含G)可能会出现迭代情况
    for i in range(len(node_val.param_list)):
        if node_val.param_list[i].val == None:
            node_val.param_list[i].val = param
            return
        elif type(node_val.param_list[i].val) == Project or type(node_val.param_list[i].val) == Select \
                or type(node_val.param_list[i].val) == In or type(node_val.param_list[i].val) == Group \
                or type(node_val.param_list[i].val) == Max or type(node_val.param_list[i].val) == Min \
                or type(node_val.param_list[i].val) == Avg or type(node_val.param_list[i].val) == Sum \
                or type(node_val.param_list[i].val) == Order or type(node_val.param_list[i].val) == Count \
                or type(node_val.param_list[i].val) == And or type(node_val.param_list[i].val) == Or \
                or type(node_val.param_list[i].val) == Modify or type(node_val.param_list[i].val) == CombineF \
                or type(node_val.param_list[i].val) == Combine or type(node_val.param_list[i].val) == Not:
            fill_arg(node_val.param_list[i].val, param)


def check_name(n1, n2):
    # 检查c_name 是否相等
    if type(n1) == list and type(n2) == list:
        if len(n1) == len(n2):
            for i in range(len(n1)):
                if n1[i] not in n2: return False
        else:
            return False
    elif type(n1) == list:
        return len(n1) == 1 and n1[0] == n2
    elif type(n2) == list:
        return len(n2) == 1 and n2[0] == n1
    else:
        return n1 == n2


def in_parameter(cls):
    for i in range(len(cls.param_list)):
        if cls.param_list[i].val != None:
            return cls.param_list[i].val.value
    return None


def check_3(param, node):
    #这个用来检查参数是子树带的时，param条件
    #可能param是c 和 f
    for i in range(len(node.param_list)):
        if node.param_list[i].val == None:
            #看看node的类型 aggerate, argmax,argmin, group
            if type(node) == Sum or type(node) == Min or type(node) == Max or type(node) == Avg or type(node)==Count:
                assert param.value == 'c'
                if param.c_type == 'number':
                    return True
                else:
                    return False
            elif type(node) == Group:
                assert param.value == 'c' or param.value == 'F'
                if param.value == 'c' and (param.c_type == 'string' or param.c_type == 'date'):  #得是number；类型
                    return True
                elif param.value == 'F' and param.c_type == 'number':
                    return True
                else:
                    return False
            elif type(node.param_list[i].val) == Project or type(node.param_list[i].val) == Select \
                         or type(node.param_list[i].val) == In or type(node.param_list[i].val) == Group \
                         or type(node.param_list[i].val) == Max or type(node.param_list[i].val) == Min \
                         or type(node.param_list[i].val) == Avg or type(node.param_list[i].val) == Sum \
                         or type(node.param_list[i].val) == Order or type(node.param_list[i].val) == Count \
                         or type(node.param_list[i].val) == And  or type(node.param_list[i].val) == Or \
                         or type(node.param_list[i].val) == Modify or type(node.param_list[i].val) == CombineF \
                         or type(node.param_list[i].val) == Combine or type(node.param_list[i].val) == Not:
                return check_3(param,node.param_list[i].val)




def check_2(n1, key):
    def is_string(t):
        for i in range(len(t)):
            if t[i] != 'string' and t[i] != 'date':return False
        return True
    #Group(c,F)(C,F)(EachFilter,F)(c,G)(C,F)(EachFilter,F)
    #argmax(c,F)
    #lambda(F).G = group(G,EachFilter)
    #lambda(F).F = argmax(c,F)       F是number类型
    if n1.value == 'c' or n1.value == 'C':
        if type(n1.c_type) == str and (n1.c_type == 'string'or n1.c_type == 'date'):return True
        elif type(n1.c_type) == list and is_string(n1.c_type):return True
        else:return False
    elif n1.value == 'F':
        if 'number' in n1.c_type:return True
        else:return False
    else:
        print(n1.c_type)
        print(key)
        raise ("parse_algorithm check_2 is non valid")

def createVal_1(cls, param, exp,key):  # 用于消参

    # cls 生成的节点的val的类型, param生成节点要的参数
    new_node_val = copy.deepcopy(cls)  # lambda(C).F
    if param.value == 'T':
        if type(param) == TClass:
            fill_arg(new_node_val,param)
            new_node_val.value = exp
            new_node_val.t_name = param.t_name
            if new_node_val.c_name == None:
                new_node_val.c_name = 'count(t)'
                new_node_val.c_type = 'number'
            else:
                new_node_val.c_name = union(new_node_val.c_name,'count(t)')
                new_node_val.c_type = union(new_node_val.c_type,'number')
            return new_node_val
        else:
            return None

    # 看下aggregate 的参数合不合法
    elif type(cls) == Sum or type(cls) == Min or type(cls) == Max or type(cls) == Avg or type(cls) == Count:  # lambda(c).F
        if type(cls) == Count and type(param) == TClass: #lambda(T).F 缺 T
            new_node_val.param.val = param
            new_node_val.value = exp
            new_node_val.t_name = param.t_name
            new_node_val.c_name = 'count(t)'  #列名
            new_node_val.c_type = 'number'
            return new_node_val
        elif type(cls) == Count:
            new_node_val.param.val = param
            new_node_val.value = exp
            new_node_val.t_name = param.t_name
            new_node_val.c_name = union(new_node_val.c_name, param.c_name)  # 列名
            new_node_val.c_type = 'number'
            return new_node_val
        elif param.c_type == 'number':
            new_node_val.param.val = param

        else:
            return None

    elif type(cls) == Select or type(cls) == Project:  # select(T,Filter) 可能缺F,c 其中c 在 T 中
        if check(cls, param) and check_3(param,cls):   #看看参数类型 可能带c , 这个c可能是 aggerate c 也可能是 argmax 和group
            fill_arg(new_node_val, param)
        else:
            return None

    elif type(cls) == Group:
        #参数有两种每种情况
        #G不可能缺EachFilter
        #所以G缺 c, C, F F可能是modify, aggerate, combineF, In
        if check_2(param, key): #就是说消参时候 c,C 必须是string 类型
            fill_arg(new_node_val, param)
        else:
            return None

    elif type(cls) == Order:
        # 如果缺dir 直接填
        if param.value == 'dir':
            new_node_val.dir = param
        elif new_node_val.t_name == None: fill_arg(new_node_val, param)
        #lambda(c,T,dir) c必须在T中

        #如果缺c 看看c在不在T中
        elif param.value == 'c':
            if check(cls,param): fill_arg(new_node_val,param)
            else:return False
        #如果缺T,
        elif param.value == 'T':
            if check(param,cls):fill_arg(new_node_val,param)
            else:return False
        else:
            print(param.value)
            raise ('Create_1 Order is not valid')

    elif type(cls) == In or type(cls) == CombineF:  #因为这两个都是F, F,N-->F 只可能是这种情况带参数
        #In 是 (c,V), (c,D), (c,N), (F,N) --> c可以是modify, 但是不带参数,
        # F可以是aggerate 可以带c, c是number
        # F可以是modify, (F, Filter) (F,EachFilter)
        # F可以是combineF 带c
        # F可以是Filter 因为F,N会生成
        assert param.value == 'c',"Create_val1 In param value is not valid {0}".format(param.value)
        flag = False #看是否填参了
        for i in range(len(cls.param_list)):
            if type(cls.param_list[i].val) == Modify: #modify 类型不能带参
                return None

            elif type(cls.param_list[i].val) == Sum or type(cls.param_list[i].val) == Min or type(cls.param_list[i].val) == Max \
                            or type(cls.param_list[i].val) == Avg or type(cls.param_list[i].val) == Count or type(cls.param_list[i].val) == In \
                    or type(cls.param_list[i].val) == CombineF:
                if param.c_type == 'number':
                    fill_arg(new_node_val,param)
                    flag = True
                    break
                else:return None
        if flag == False:  #说明没有填参成功
            print(type(cls.param_list[0].val))
            print(type(cls.param_list[1].val))
            raise ("CreateVal_1 In option is not valid ")


    elif type(cls) == Combine or type(cls) == And or type(cls) == Or or type(cls) == Not or type(cls) == Modify:
        return None
    else:
        print(type(cls))
        print(key)
        raise ("CreateVal_1 option is not valid ")
    new_node_val.value = exp
    new_node_val.t_name = param.t_name
    # 消参应该是取并集
    new_node_val.c_name = union(new_node_val.c_name, param.c_name)
    new_node_val.c_type = union(new_node_val.c_type, param.c_type)
    return new_node_val



def check(n1, n2):
    n1_c, n2_c = n1.c_name, n2.c_name
    if type(n1_c) == list and type(n2_c) == list:
        # 看看n2是不是全在n1里
        for i in range(len(n2_c)):
            if n2_c[i] not in n1_c: return False
    elif type(n1_c) == list:
        if n2_c not in n1_c: return False
    elif type(n2_c) == list:
        if len(n2_c) != 1 or n2_c[0] != n1_c: return False
    return True


def createVal_2(node1, node2, option, exp):  # lambda(F).G T --> lambda(F).T=project(G,T)
    option = extract_option(option)
    cls = get_opt(option)
    if cls == None:
        return cls
    # 这个只能是两个参数的操作
    assert len(cls.param_list) == 2, "CreateVal_2 param_list len is wrong:{0}".format(len(cls.param_list))
    # 这个不用check条件 就是填变量
    cls.param_1.val = node1
    cls.param_2.val = node2

    cls.value = exp
    cls.t_name = node1.t_name if node1.t_name != None else node2.t_name
    cls.c_name = union(node1.c_name, node2.c_name)
    cls.c_type = union(node1.c_type, node2.c_type)
    return cls


def createVal_3(node1, node2, option, exp, key):
    def checkCClass(l):
        t_names = []
        for i in range(len(l)):
            if l[i].t_name not in t_names:
                t_names.append(l[i].t_name)
            if len(t_names) == 2: return False
        return True

    def generate(mode):
        l = []
        if type(node1) == mode:
            l.extend(node1.c_list)
            l.append(node2)
        elif type(node2) == mode:
            l.extend(node2.c_list)
            l.append(node1)
        else:
            l.append(node1)
            l.append(node2)
        return l

    # 这个option可能是空
    if option == None:
        if exp == 'C':
            l = generate(CClass)
            if checkCClass(l):
                cls = CClass(l)
            else:
                return None
        else:
            raise ('CreateVal_3 is error when option is None : {0}'.format(exp))
        return cls
    else:
        option = extract_option(option)
        cls = composition(node1, node2, option, exp, key)
        return cls


def bottom_up_parser(node1, node2, gDict,key):
    g = []
    # 两种和并的方式 1 填写参数, 2 根据grammar
    # 先看填写参数的方式, 填写参数方式表达式中得有lambda

    # 讨论根据grammar往上建树
    nodes = []
    for (rhs, lhs, func) in gDict:
        rhs = rhs.split(',')
        # 只有一个order带3个参数,但sort的lambda,所以只考虑两个参数的情况
        if len(rhs) == 2:
            if (node1.val.value == rhs[0] and node2.val.value == rhs[1]) or (
                    node1.val.value == rhs[1] and node2.val.value == rhs[0]):
                gene = createVal_3(node1.val, node2.val, func, lhs,key)
                if gene == None: continue
                node = Node(node1, node2, gene, node1.start, node2.end)
                nodes.append(node)
    if nodes != []:
        l = nodes
        g += l
    return g