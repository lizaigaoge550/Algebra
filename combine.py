from utils import extract_option,union
from utils import get_opt
from opt_class import *

def check(n1,n2):
    #先找出T value
    # 取出n1,n2的c_name
    n1_c, n2_c = n1.c_name, n2.c_name
    T = None
    if 'T' in n1.value:
        T = n1
        if type(n1_c) == list and type(n2_c) == list:
            #看看n2是不是全在n1里
            for i in range(len(n2_c)):
                if n2_c[i] not in n1_c: return (False,T,n2)
        elif type(n1_c) == list:
            if n2_c not in n1_c: return (False,T,n2)
        else:
            return (n1_c == n2_c,T,n2)
    elif 'T' in n2.value:
        T = n2
        if type(n1_c) == list and type(n2_c) == list:
            #看看n1是不是全在n2里
            for i in range(len(n1_c)):
                if n1_c[i] not in n2_c: return (False, T, n1)
        elif type(n2_c) == list:
            if n1_c not in n2_c:return (False,T,n1)
        else:
            return (n1_c == n2_c,T,n1)
    else: raise("Check not valid no T")
    if T == n1:
        return (True,T,n2)
    else:
        return (True,T,n1)


def check_2(n1,n2):
    def is_string(t):
        for i in range(len(t)):
            if t[i] != 'string' and t[i] != 'date':return False
        return True
    #Group(c,F)(C,F)(EachFilter,F)(c,G)(C,F)(EachFilter,F)
    #argmax(c,F)
    if n1.value == 'c' or n1.value == 'C':
        if type(n1.c_type) == str and (n1.c_type == 'string' or n1.c_type == 'date'):return True
        elif type(n1.c_type) == list and is_string(n1.c_type):return True
        else:return False
    elif n2.value == 'c' or n2.value == 'C':
        if type(n2.c_type) == str and (n2.c_type == 'string' or n2.c_type == 'date'):return True
        elif type(n2.c_type) == list and is_string(n2.c_type):return True
        else:return False
    else:
        print("n1 value {0}, n2 value {1}".format(n1.value,n2.value))
        raise("check_2 is not valid")




def composition(node1,node2,option,exp, key): #lambda(F).G T --> lambda(F).T=project(G,T)
    #project --> (c,T), (C,T), (G,T), (F,T), 其中(T可以说 lambda(F).T=project(G,T).... G可以是lambda(F).G=group(F,c|C))
    #select --> (Filter, T) 其中(Filter 可以说lambda(c).Filter=In(c,V))
    #aggregate --> max, min, sum, avg 这个只是带一个参数c 不符合
    #In --> (c,V),(c,D),(c,N), (F,N)
    #group --> (F,C|c), (F,EachFilter), (G,C|c) (G,EachFilter)

    #Add --> (Filter, Filter)
    #Or --> (Filter, Filter)
    #EachFilter --> combine(Filter,Filter)
    #F --> combineF(F,F)
    #Order --> (c,T)
    #先根据option确定 是什么类
    option = extract_option(option)
    #cls = dic.get(option, None)  # Project
    cls = get_opt(option)
    if cls == None:
        #raise ("Error OPtion {0}".format(option))
        return cls
    #这个只能是两个参数的操作
    assert len(cls.param_list) == 2,"CreateVal_2 param_list len is wrong:{0}".format(len(cls.param_list))
    #check 合并条件是否符合

    #如果参数已知，只有project会缩小表
    if type(cls) == Select or type(cls) == Order or type(cls) == Project: #条件 node1.c_name 在 node2.c_name 中
        t,f,c = check(node1,node2)
        if t == True:
            cls.param_1.val = node1
            cls.param_2.val = node2
            cls.value = exp
            cls.t_name = c.t_name
            #交集
            if type(cls) == Project:
                cls.c_name = c.c_name
                cls.c_type = c.c_type
            else:
                cls.c_name = f.c_name
                cls.c_type = f.c_type
        else:return None

    elif type(cls) == Group: #(c,F), (F,C|c), (G,C|c)
        if node1.t_name == node2.t_name:
            if check_2(node1,node2): #最重要的是(c,F,EachFilter 是string类型)
                cls.param_1.val = node1
                cls.param_2.val = node2
                cls.value = exp
                cls.t_name = node1.t_name
                cls.c_name = union(node1.c_name, node2.c_name)
                cls.c_type = union(node1.c_type, node2.c_type)
            else:
                return None
        else:return None

    elif type(cls) == In:
        if node1.value == 'N' or node2.value == 'N':
            try:
                if 'number' in node1.c_type and 'number' in node2.c_type: #F可能是combineF ,所以用 in
                    cls.param_1.val = node1
                    cls.param_2.val = node2
                    cls.value = exp
                    cls.t_name = node1.t_name if node1.t_name != None else node2.t_name
                    cls.c_name = union(node1.c_name,node2.c_name)
                    cls.c_type = union(node1.c_type,node2.c_type)
                else:return None
            except:
                print(key)
                exit(101)
        elif node1.value == 'D' or node2.value == 'D': #只能是c,D
            if  node1.c_type == 'date' and node2.c_type == 'date': #只能是c,D所以用 == 而不是 in
                cls.param_1.val = node1
                cls.param_2.val = node2
                cls.value = exp
                cls.t_name = node1.t_name if node1.t_name != None else node2.t_name
                cls.c_name = union(node1.c_name,node2.c_name)
                cls.c_type = union(node1.c_type,node2.c_type)
            else:return None

        elif node2.value == 'blank' or node1.value == 'blank':
            cls.param_1.val = node1
            cls.param_2.val = node2
            cls.t_name = node1.t_name if node1.t_name != None else node2.t_name
            cls.value = exp
            if node1.value == 'c':
                cls.c_name = node1.c_name
                cls.c_type = node1.c_type

            elif node2.value == 'c':
                cls.c_name = node2.c_name
                cls.c_type = node2.c_type
            else:
                return None

        else:
            if node1.t_name == node2.t_name and node1.c_name == node2.c_name: #这个是c,V 判断条件
                cls.param_1.val = node1
                cls.param_2.val = node2
                cls.value = exp
                cls.t_name = node2.t_name
                cls.c_name = node2.c_name
                cls.c_type = node2.c_type
            else:return None


    elif type(cls) == Not:
        #有两种情况 1-->c, Blank, 2-->Filter, Excluding
        # if (node1.value == 'c' and node2.value == 'blank') or (node1.value == 'blank' and node2.value == 'c'):
        #     cls.param_1.val = node1
        #     cls.param_2.val = node2
        #     if node1.value == 'c':
        #         cls.c_name = node1.c_name
        #         cls.c_type = node1.c_type
        #     else:
        #         cls.c_name = node2.c_name
        #         cls.c_type = node2.c_type
        if (node1.value == 'Filter' and node2.value == 'Excluding') or (node2.value == 'Filter' and node1.value == 'Excluding'):
            cls.param_1.val = node1
            cls.param_2.val = node2
            cls.value = exp
            cls.t_name = node1.t_name if node1.t_name != None else node2.t_name
            if node1.value == 'Filter':
                cls.c_name = node1.c_name
                cls.c_type = node1.c_type
            else:
                cls.c_name = node2.c_name
                cls.c_type = node2.c_type
        else:
            return None

    elif type(cls) == And or type(cls) == Or:
        assert node1.value == 'Filter' and node2.value == 'Filter' #BMW and X5 ()
        if node1.t_name == node2.t_name: #and node1.c_name != node2.c_name:
            cls.param_1.val = node1
            cls.param_2.val = node2
            cls.value = exp
            cls.t_name = node1.t_name
            cls.c_name = union(node1.c_name, node2.c_name)
            cls.c_type = union(node1.c_type, node2.c_type)
        else:
            return None

    elif type(cls) == Combine: #EachFilter -- Filter Filter. EachFilter -- c,V, EachFilter --> c.D
        #assert (node1.value == 'Filter' and node2.value == 'Filter')
        if node1.c_name == node2.c_name and (node1.c_type == 'string' or node1.c_type == 'date'):
            cls.param_1.val = node1
            cls.param_2.val = node2
            cls.value = exp
            cls.t_name = node1.t_name
            cls.c_name = node1.c_name
            cls.c_type = node1.c_type
        else:
            return None

    elif type(cls) == Modify: #Filter c -- > c, Filter F --> F, Filter G --> G
        # node1 和 node2 如果是F不能是argmax or argmin or sum or count 因为这些函数执行为就一个数, 没办法Filter
        #if node1.value == 'F' and (type(node1) == Argmin or type(node1) == Argmax or type(node1)==Count or type(node1)==Sum): return None

        #if node2.value == 'F' and (type(node2) == Argmin or type(node2) == Argmax or type(node1)==Count or type(node1)==Sum): return None

        #现在也可以是 EachFilter, c -> c , EachFilter, F --> F,
        #两种情况 一种是 F,G (Filter 和 EachFilter的操作一样)
        if (node1.value == 'F' or node1.value == 'G' or node1.value == 'c') or (node2.value == 'F' or node2.value == 'G' or node2.value == 'c'):
            if node1.c_name != node2.c_name:
                cls.param_1.val = node1
                cls.param_2.val = node2
                cls.value = exp
                cls.t_name = node1.t_name
                if node1.value == 'c' or node1.value == 'F' or node1.value == 'G':
                    cls.c_name = node1.c_name
                    cls.c_type = node1.c_type
                    cls.description = node1.description
                elif node2.value == 'c' or node2.value == 'F' or node2.value == 'G':
                    cls.c_name = node2.c_name
                    cls.c_type = node2.c_type
                    cls.description = node2.description
            else:
                return None
        else:
            return None



    elif type(cls) == CombineF:
        #直接合并
        cls.param_1.val = node1
        cls.param_2.val = node2
        cls.value = exp
        cls.t_name = node1.t_name
        cls.c_name = union(node1.c_name, node2.c_name)
        cls.c_type = union(node1.c_type, node2.c_type)

    else:
        print(type(cls))
        raise('Compostion option is not val '+ (type(cls)))

    return cls