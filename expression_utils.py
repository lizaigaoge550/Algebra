#coding=utf-8
from opt_class import *
from class_file import *
def check(root):
    aggerateList = [Avg,Count,Max,Min,Sum]
    if type(root) == In:
        #如果参数是cclass Vclass NClass
        if type(root.param_list[0].val) == cClass and (type(root.param_list[1].val) == VClass or type(root.param_list[1].val) == NClass):
            return True
        if  type(root.param_list[1].val) == cClass and (type(root.param_list[0].val) == VClass or type(root.param_list[0].val) == NClass):
            return True
        #参数是aggerate Nclass
        if type(root.param_list[0].val) in aggerateList and (type(root.param_list[1]) == NClass):
            return True
        if type(root.param_list[1].val) in aggerateList and (type(root.param_list[0]) == NClass):
            return True
    return False
