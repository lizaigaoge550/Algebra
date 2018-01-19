from __future__ import print_function
from class_file import *
from opt_class import *
from node import Node
from generate_rule import generateRule
import os
from getTable import get_table

s = ''

'G --> T Project'
'C|c -- > T Proejct'
'F --> T Project'
'Filter --> T Select'
pattern = ['G','C','c','F','Filter']
globalagg = ""
globalc = ""
t_name,Table = get_table()
def postprocessing(dic,length):
    new_node = []
    for root in dic[0][length]:
        if 'lambda' in root.val.value: continue
        elif root.val.value == 'T': new_node.append(root)
        elif root.val.value in pattern:
            if root.val.value == 'Filter':
                opt = Select(None,None,None)
            else:
                opt = Project(None,None,None)
            opt.param_1.val = root.val
            opt.c_name = root.val.c_name
            opt.t_name = root.val.t_name
            opt.c_type = root.val.c_type
            # 第二个参数是T
            t = TClass(root.val.t_name, root.val.c_name, root.val.c_type)
            opt.param_2.val = t
            opt.value = 'T'
            n = Node(root,None,opt,root.start,root.end)
            new_node.append(n)
            #dic[0][length].append(n)

    return new_node
    #generate_expression(dic,length)


def dfs(value,key):
    global s
    if value.description != None and type(value) != Modify and type(value) != CClass  :
        if type(value.description) == list:
            try:
                s += '(' + ",".join(value.description)+ ')'
            except:
                print(key)
        else:
            s += '(' + value.description+ ')'
        return
    else:
        s += '(' + type(value).__name__
    for i in range(len(value.param_list)):
        if value.param_list[i].val != None:
            dfs(value.param_list[i].val,key)
    s += ')'

def generate_expression(dic,length,file_name):
    global s
    f = os.path.join('job_result',file_name)
    fw = open(f,'w')
    fw.write(file_name+'\n\n')
    #log = {}
    c = 0
    for root in dic[0][length]:
        if 'lambda' not in root.val.value:
            s = ""
            dfs(root.val,file_name)
            c += 1
            fw.write(s+'\n')
        #log[file_name] = c
    if c == 0:
        #print(file_name)
        print(file_name,file=open('non_analysis','a'))
    fw.write("count : "+ str(c)+'\n')
    fw.flush()
    fw.close()
    return c


res = {'from':[],'select':[],'where':[],'orderby':[],'groupby':[]}

def init():
    global res
    for k, v in res.items():
        res[k] = []


def findAggerateFandc(parameter):
    global globalagg,globalc
    #assert type(parameter) == In,('findAggerateFandc parameter is not Filter')
    if type(parameter) == NClass:
        return


    if type(parameter) == cClass or type(parameter) == TClass:
        globalc = parameter.description
        return

    if type(parameter) == Min or type(parameter) == Max or type(parameter) == Avg or type(parameter) == Count or type(parameter) == Sum:
        globalagg = type(parameter).__name__

    for i in range(len(parameter.param_list)):
        findAggerateFandc(parameter.param_list[i].val)



def slotFilling(parameter, parentType, default, key): #这个默认的值代表N
    # 看看是什么操作类型
    #基本的操作 c, T, F(aggerate), Filter(In(c,N), In(c,V), In(F,N))
    #其中 c(可选参数) 父节点是argmax or argmin or group 填到 res[Select], res[groupby]中 否则填到 res[Select]中
    #F(aggerate) 有可选参数根据parentType 决定, 当parentType 不是 argmin or argmax 则填到 select中, else 填到 orderby中
    #Filter 肯定是要填入 res[Where] 有可选参数 如果父节点是EachFilter col 填到 res[groupby] 中
    if type(parameter) == TClass:
        if parameter.description not in res['from']:
            res['from'].append(parameter.description)
        return

    if type(parameter) == NClass or type(parameter) == VClass:
        print(key)
        exit(200)

    elif type(parameter) == ExcludeClass:
        return

    elif type(parameter) == cClass:
        if default != None:
            assert type(default) == DClass or type(default) == NClass or type(default) == VClass or type(default) == BlankClass
            flag = False
            for i in range(len(res['where'])):
                if parameter.description in res['where'][i]:
                    if type(default) == NClass:
                        res['where'][i][parameter.description].append(
                            default.description)
                    elif type(default) == DClass:
                        res['where'][i][parameter.description].append(
                            default.description)
                    elif type(default) == BlankClass:
                        res['where'][i][parameter.description].append(
                            default.description)
                    else:
                        res['where'][i][parameter.description].append(
                            default.description.split('.')[-1])
                    flag = True

            if flag == False:
                d = {}
                if type(default) == NClass:
                    d[parameter.description] = [default.description]
                elif type(default) == DClass:
                    d[parameter.description] = [default.description]
                elif type(default) == BlankClass:
                    d[parameter.description] = [default.description]
                else:
                    d[parameter.description] = [default.description.split('.')[-1]]
                res['where'].append(d)
            #return #有条件的c只在where中 如果和Eachfilter 放到select和groupby中
            if parentType == Combine:
                if parameter.description not in res['select']:
                    # raise('cClass value repeat!!!')
                    res['select'].append(parameter.description)
                if parameter.description not in res['groupby']:
                    res["groupby"].append(parameter.description)
                return
            else:
                return

        else:
            if parentType == Min or parentType == Max or parentType == Avg or parentType == Count or parentType == Sum:
                return

            if parameter.description not in res['select']:
                #raise('cClass value repeat!!!')
                res['select'].append(parameter.description)

            if parentType == Group or parentType == Combine:
                #填到groupby中
                if parameter.description not in res['groupby']:
                    res["groupby"].append(parameter.description)
            return


    #aggerate 操作 f 的 c 可能是cclass 也可能是 c: modify 但是都有description
    elif type(parameter) == Sum or type(parameter) == Min or type(parameter) == Max or type(parameter) == Avg or type(parameter) == Count:
        if type(parameter.param.val) != cClass and type(parameter.param.val) != TClass:
            iteration(parameter.param.val,key,parentType=type(parameter))

        if default != None and type(default) == NClass:
            flag = False
            v = parameter.param.val.description + '.'+type(parameter).__name__.lower()
            for i in range(len(res['where'])):
                if v in res['where'][i]:
                    res['where'][i][v].append(default.description)
                    flag = True
            if flag == False:
                d = {}
                d[v] = [default.description]
                res['where'].append(d)

            if parentType == Group:
                if parameter.param.val.description + '.' + type(parameter).__name__.lower() not in res['select']:
                    # raise("Aggregate Select value repeat!!!")
                    res['select'].append(parameter.param.val.description + '.' + type(parameter).__name__.lower())
            #return #有条件的F只在where里面就行 #只要是 F都放到 select中


        if parameter.param.val.description+'.'+type(parameter).__name__.lower() not in res['select']:
            #raise("Aggregate Select value repeat!!!")
            res['select'].append(parameter.param.val.description+'.'+type(parameter).__name__.lower())
        return


    #Filter操作 c , F有可能是modify Filter 可能是 c 和 blank , (excluding 和 filter)
    elif type(parameter) == In or type(parameter) == Combine:
        global globalc, globalagg
        #首先得填到where中
        # where 是 一个list， list中的每个元素是一个dict
        if (parameter.param_list[0].val.value == 'c' and parameter.param_list[1].val.value == 'V'):
            if (type(parameter.param_list[0].val) != cClass): #那么c就是modify
                #看看要不要更新parentType
                if (parentType == Group or parentType == Combine):
                    return iteration(root=parameter.param_list[0].val,parentType=parentType,default=parameter.param_list[1].val,key=key)
                else:
                    return iteration(root=parameter.param_list[0].val, default=parameter.param_list[1].val,key=key)


            flag = False
            for i in range(len(res['where'])):
                if parameter.param_list[0].val.description in res['where'][i]:
                    # {"SharkAttack.Fatality": ["fatal"]}
                    if parentType == Not:
                        res['where'][i][parameter.param_list[0].val.description].append(
                            "Excluding "+ parameter.param_list[1].val.description.split('.')[-1])
                    else:
                        res['where'][i][parameter.param_list[0].val.description].append(parameter.param_list[1].val.description.split('.')[-1])
                    flag = True
            if flag ==  False:
                d = {}
                if parentType == Not:
                    d[parameter.param_list[0].val.description] = ["Excluding " + parameter.param_list[1].val.description.split('.')[-1]]
                else:
                    d[parameter.param_list[0].val.description] = [
                        parameter.param_list[1].val.description.split('.')[-1]]
                res['where'].append(d)


            if parentType == Combine:  #EachFilter
                if parameter.param_list[0].val.description not in res['select']:
                    res['select'].append(parameter.param_list[0].val.description)
                if parameter.param_list[0].val.description not in res['groupby']:
                    res['groupby'].append(parameter.param_list[0].val.description)
            return
        #c, V
        elif (parameter.param_list[0].val.value == 'V' and parameter.param_list[1].val.value == 'c'):
            if (type(parameter.param_list[1].val) != cClass):
                if (type(parameter.param_list[0].val) != cClass):
                    # 看看要不要更新parentType
                    if (parentType == Group or parentType == Combine):
                        return iteration(root=parameter.param_list[1].val, key = key,parentType=parentType,
                                         default=parameter.param_list[0].val)
                    else:
                        return iteration(parameter.param_list[1].val, parameter.param_list[0].val)
            flag = False
            for i in range(len(res['where'])):
                if parameter.param_list[1].val.description in res['where'][i]:
                    if parentType == Not:
                        res['where'][i][parameter.param_list[1].val.description].append(
                            "Excluding "+parameter.param_list[0].val.description.split('.')[-1])
                    else:
                        res['where'][i][parameter.param_list[1].val.description].append(parameter.param_list[0].val.description.split('.')[-1])
                    flag = True

            if flag == False:
                d = {}
                if parentType == Not:
                    d[parameter.param_list[1].val.description] = ["Excluding "+parameter.param_list[0].val.description.split('.')[-1]]
                else:
                    d[parameter.param_list[1].val.description] = [parameter.param_list[0].val.description.split('.')[-1]]
                res['where'].append(d)


            if parentType == Combine:  #EachFilter
                if parameter.param_list[1].val.description not in res['select']:
                    res['select'].append(parameter.param_list[1].val.description)
                if parameter.param_list[1].val.description not in res['groupby']:
                    res['groupby'].append(parameter.param_list[1].val.description)
            return
        #c,D 父节点肯定不会是EachFilter, 现在可以了
        elif (parameter.param_list[0].val.value == 'c' and parameter.param_list[1].val.value == 'D'):
            if (type(parameter.param_list[0].val) != cClass):
                if (parentType == Group or parentType == Combine):
                    return iteration(parameter.param_list[0].val,key=key, parentType=parentType, default=parameter.param_list[1].val)
                else:
                    return iteration(root=parameter.param_list[0].val, default=parameter.param_list[1].val,key=key)

            flag = False
            for i in range(len(res['where'])):
                if parameter.param_list[0].val.description in res['where'][i]:
                    if parentType == Not:
                        res['where'][i][parameter.param_list[0].val.description].append(
                            "Excluding "+parameter.param_list[1].val.description)
                    else:
                        res['where'][i][parameter.param_list[0].val.description].append(parameter.param_list[1].val.description)
                    flag = True
            if flag == False:
                d = {}
                if parentType == Not:
                    d[parameter.param_list[0].val.description] = ["Excluding " + parameter.param_list[1].val.description]
                else:
                    d[parameter.param_list[0].val.description] = [parameter.param_list[1].val.description]
                res['where'].append(d)

            if parentType == Combine:  #EachFilter
                if parameter.param_list[0].val.description not in res['select']:
                    res['select'].append(parameter.param_list[0].val.description)
                if parameter.param_list[0].val.description not in res['groupby']:
                    res['groupby'].append(parameter.param_list[0].val.description)
            return
        # c,D
        elif (parameter.param_list[1].val.value == 'c' and parameter.param_list[0].val.value == 'D'):
            if (type(parameter.param_list[1].val) != cClass):
                if parentType == Group or parentType == Combine:
                    return iteration(parameter.param_list[1].val,parentType=parentType,default=parameter.param_list[0].val,key=key)
                else:
                    return iteration(root=parameter.param_list[1].val, default=parameter.param_list[0].val, key=key)

            flag = False
            for i in range(len(res['where'])):
                if parameter.param_list[1].val.description in res['where'][i]:
                    if parentType == Not:
                        res['where'][i][parameter.param_list[1].val.description].append(
                            "Excluding " + parameter.param_list[0].val.description)
                    else:
                        res['where'][i][parameter.param_list[1].val.description].append(parameter.param_list[0].val.description)
                    flag = True
            if flag == False:
                d = {}
                if parentType == Not:
                    d[parameter.param_list[1].val.description] = ["Excluding " + parameter.param_list[0].val.description]
                else:
                    d[parameter.param_list[1].val.description] = [parameter.param_list[0].val.description]
                res['Where'].append(d)
            if parentType == Combine:  #EachFilter
                if parameter.param_list[1].val.description not in res['select']:
                    res['select'].append(parameter.param_list[1].val.description)
                if parameter.param_list[1].val.description not in res['groupby']:
                    res['groupby'].append(parameter.param_list[1].val.description)
            return

        #c,N
        elif (parameter.param_list[0].val.value == 'c' and (parameter.param_list[1].val.value == 'N' or parameter.param_list[1].val.value == 'blank')):
            if (type(parameter.param_list[0].val) != cClass): return iteration(parameter.param_list[0].val,default=parameter.param_list[1].val,key=key)
            flag = False
            for i in range(len(res['where'])):
                if parameter.param_list[0].val.description in res['where'][i]:
                    if parentType == Not:
                        res['where'][i][parameter.param_list[0].val.description].append(
                            "Excluding " + parameter.param_list[1].val.description)
                    else:
                        res['where'][i][parameter.param_list[0].val.description].append(parameter.param_list[1].val.description)
                    flag = True
            if flag == False:
                d = {}
                if parentType == Not:
                    d[parameter.param_list[0].val.description] = ["Excluding " + parameter.param_list[1].val.description]
                else:
                    d[parameter.param_list[0].val.description] = [parameter.param_list[1].val.description]
                res['where'].append(d)
            return

        # c,N
        elif (parameter.param_list[1].val.value == 'c' and (parameter.param_list[0].val.value == 'N' or parameter.param_list[0].val.value == 'blank') ):
            if (type(parameter.param_list[1].val) != cClass): return iteration(parameter.param_list[1].val,default=parameter.param_list[0].val,key=key)
            flag = False
            for i in range(len(res['where'])):
                if parameter.param_list[1].val.description in res['where'][i]:
                    if parentType == Not:
                        res['where'][i][parameter.param_list[1].val.description].append(
                            "Excluding " + parameter.param_list[0].val.description)
                    else:
                        res['where'][i][parameter.param_list[1].val.description].append(
                            parameter.param_list[0].val.description)
                    flag = True
            if flag == False:
                d = {}
                if parentType == Not:
                    d[parameter.param_list[1].val.description] = ["Excluding " + parameter.param_list[0].val.description]
                else:
                    d[parameter.param_list[1].val.description] = [parameter.param_list[0].val.description]
                res['where'].append(d)
            return

        #F,N F可能是modify 也可能是combineF 也可能是 F(Filter)
        elif (parameter.param_list[0].val.value.split('.')[-1] == 'F'  and parameter.param_list[1].val.value == 'N'):

            if type(parameter.param_list[0].val) == Modify or type(parameter.param_list[0].val) == CombineF:
                return iteration(parameter.param_list[0].val, parentType=parentType,
                                 default=parameter.param_list[1].val, key=key)
            elif type(parameter.param_list[0].val) == In:
                iteration(parameter.param_list[0].val, parentType=parentType, default=parameter.param_list[1].val,
                          key=key)

            if type(parameter.param_list[0].val) == In:
                globalc = ""
                globalagg = ""
                # 找到一个aggrate F 和 对应c
                findAggerateFandc(parameter.param_list[0].val)
                value = globalc + '.' + globalagg.lower()
            else:
                firstpara = parameter.param_list[0].val.param.val
                if type(firstpara) != cClass and type(firstpara) != TClass:
                    iteration(parameter.param_list[0].val,key) #这里不要return 因为这里是这个F(aggerate类型) 和 N产生关系, 所以要接着往下执行
                value = parameter.param_list[0].val.param.val.description + '.' + type(parameter.param_list[0].val).__name__.lower()
            flag = False
            for i in range(len(res['where'])):
                if value in res['where'][i]:
                    if parentType == Not:
                        res['where'][i][value].append("Excluding " + parameter.param_list[1].val.description)
                    else:
                        res['where'][i][value].append(parameter.param_list[1].val.description)
                    flag = True
            if flag == False:
                d = {}
                if parentType == Not:
                    d[value] = ["Excluding " + parameter.param_list[1].val.description]
                else:
                    d[value] = [parameter.param_list[1].val.description]
                res['where'].append(d)

            #if parentType == Group:  #EachFilter
            if value not in res['select']:
                res['select'].append(value)
            return

        #F,N
        elif (parameter.param_list[1].val.value.split('.')[-1] == 'F' and parameter.param_list[0].val.value == 'N'):
            if type(parameter.param_list[1].val) == Modify or type(parameter.param_list[1].val) == CombineF:
                return iteration(parameter.param_list[1].val,parentType=parentType, default=parameter.param_list[0].val,key=key)
            elif type(parameter.param_list[1].val) == In:
                iteration(parameter.param_list[1].val, parentType=parentType, default=parameter.param_list[0].val,key=key)

            #parameter.param_list[1].val 有可能是F(Filter)
            if type(parameter.param_list[1].val) == In:
                globalc = ""
                globalagg = ""
                #找到一个aggrate F 和 对应c
                findAggerateFandc(parameter.param_list[1].val)
                value = globalc+'.'+globalagg.lower()
            else:
                firstpara = parameter.param_list[1].val.param.val
                if type(firstpara) != cClass and type(firstpara) != TClass:
                    iteration(parameter.param_list[1].val,key)
                value = parameter.param_list[1].val.param.val.description + '.' + type(parameter.param_list[1].val).__name__.lower()
            flag = False
            for i in range(len(res['where'])):
                if value in res['where'][i]:
                    if parentType == Not:
                        res['where'][i][value].append("Excluding " + parameter.param_list[0].val.description)
                    else:
                        res['where'][i][value].append(parameter.param_list[0].val.description)
                    flag = True
            if flag == False:
                d = {}
                if parentType == Not:
                    d[value] = ["Excluding " + parameter.param_list[0].val.description]
                else:
                    d[value] = [parameter.param_list[0].val.description]
                res['where'].append(d)
            #if parentType == Group:  #EachFilter
            if value not in res['select']:
                res['select'].append(value)

            return


    for i in range(len(parameter.param_list)):
        # 更新parentType
        #And, Or, Combine, G, CombineF, Argmax Argmin, Modify
        #如果是 这个类型是G, Combine, Argmax Argmin 则更新
        #para = parameter.param_list[i].val
        if type(parameter.param_list[i].val) == Group or type(parameter.param_list[i].val) == Combine or \
                type(parameter.param_list[i].val) == Not:
            slotFilling(parameter.param_list[i].val, type(parameter.param_list[i].val), None, key)

        elif (type(parameter) == Group or type(parameter) == Combine or type(parameter) == Not): #当前节点类型
             slotFilling(parameter.param_list[i].val,type(parameter),None,key)

        elif parentType == Group or parentType == Combine or parentType == Not or parentType == Count or \
            parentType == Avg or parentType == Sum or parentType ==  Min or parentType == Max: #父节点类型
            slotFilling(parameter.param_list[i].val,parentType,None,key)

        else:
             slotFilling(parameter.param_list[i].val,type(parameter.param_list[i].val),None,key) #随意就按就近类型


def  iteration(root,key,parentType=None,default=None):
    global res
    currentType = type(root) if parentType == None else parentType
    try:
        if type(root) == In: slotFilling(root,currentType,default,key)
        else:
            for i in range(len(root.param_list)):
                slotFilling(root.param_list[i].val, currentType, default,key)
    except Exception as e:
        print(key)
        print(e)
        exit(1000)


import json
import re
def output_sql_tree(new,res,node,key,file_name):
    global s
    s = ''
    dfs(node.val,key)
    file_name = re.sub("[\.\!\/_,$%^*?(+\"\']+|[+——！，。？、~@#￥%……&*（）]", "",file_name)
    f = open(os.path.join('sql_tree',file_name),'a',encoding='utf-8')

    f.write(s+'\n')
    f.write("orig : {0}".format(res)+'\n')
    f.write('\n')
    f.write("new : {0}".format(new)+'\n')
    f.write('\n\n')
    f.write('\n')



def  generate_dict(dic,length, key, true_sql):
    global res
    new_node = postprocessing(dic,length)
    #fw = open(os.path.join('sql_generate', key), 'a')
    #fw.write(key+'\n\n')
    non = open('error_1','a')
    #proportion = open('proportion.txt','a')
    flag = False

    for root in new_node:
        assert root.val.value == 'T'
        init()
        if type(root.val) == TClass:
            res['select'].append(t_name)

        else:
            iteration(root.val,key)
                    #json.dump(res,fw)

        if res['select'] == [] and res['where'] == []:res['select'].append(t_name)
        #输出节点和对应的sql
        arg1,arg2 = compare(res,true_sql,key)
        if  arg1:
            flag = True
            #correct += 1
                #fw.write('\n')
        output_sql_tree(arg2, res, root, key, key)
    if flag == False:
        non.write(key+'\n')
    #fw.close()
    # if flag == True:
    #     proportion.write(key+'\n')
    #     proportion.write("sum: {0}, correct : {1}, proportion : {2}".format(sum_len,correct,correct/sum_len))
    #     #proportion.write(str(correct/sum_len))
    #     proportion.write('\n')
    #     if sum_len == correct:print(sum_len)

def putPatch(predict):
    #用来把where中的max, min 加到select 和 groupby中
    for where_index in range(len(predict['where'])):
        for key, value in predict['where'][where_index].items():
            if 'max' in value or 'min' in value:
                if len(key.split('.')) == 3:
                    col = key.split('.')[1]
                    if Table[col] == 'string':
                        #判断在不在select 和 groupby中
                        key_key = ".".join(key.split('.')[:-1])
                        if key not in predict['select']:
                            predict['select'].append(key)
                        if key_key not in predict['select']:
                            predict['select'].append(key_key)
                        if key_key not in predict['groupby']:
                            predict['groupby'].append(key_key)
    return predict

def compareList(a,b):
    #首先看长度相等不
    if a == [] and b == [[]]:return True
    if a == [[]] and b == []:return True
    if(len(a) == len(b)):
        if len(a) == 0: return True
        for i in range(len(a)):
            if a[i] not in b:
                return False
        return True
    else:
        return False


def compareDict(a,b):
    dica = {}
    dicb = {}
    # 首先把a 和 b合成一个 dict
    for i in range(len(a)):
        for k,v in a[i].items():
            dica[k] = v
    for i in range(len(b)):
        for k,v in b[i].items():
            dicb[k] = v
    for k,v in dica.items():
        if k not in dicb:
            return False
        else:
            if not compareList(v,dicb[k]):return False
    return True

def clear(t):
    #count(*)只可能出现select, orderby, where中
    if len(t['select']):
        for i in range(len(t['select'])):
            if '(' in t['select'][i]:
                t['select'][i] = t['select'][i][:t['select'][i].index('(')]
    if t['orderby'] != [[]]:
        for i in range(len(t['orderby'])):
            if '(' in t['orderby'][i][0]:
                t['orderby'][i][0] = t['orderby'][i][0][:t['orderby'][i][0].index('(')]
    if len(t['where']):
        s = []
        for i in range(len(t['where'])):
            dic = {}
            for k,v in t['where'][i].items():
                if '(' in k:
                    k = k[:k.index('(')]
                    dic[k] = v
                else:
                    dic[k] = v
            s.append(dic)
        t['where'] = s
    return t


def type_consistent(predict):
    def fun(ziduan):
        for i in range(len(predict[ziduan])):
            if type(predict[ziduan][i]) == list:
                for j in predict[ziduan][i]:
                    dic[ziduan].append(j)
            else:
                dic[ziduan].append(predict[ziduan][i])
    dic = {'select':[], 'groupby':[], 'where':[]}
    dic['orderby'] = predict['orderby']
    fun('select')
    fun('groupby')
    fun('where')
    return dic


def sum_count_transform(predict):
    for i in range(len(predict['select'])):
        l = predict['select'][i].split('.')
        if l[-1] == 'count' or l[-1] == 'sum':
            if len(l) == 2: #说明就是表
                l[-1] = 'count'
                predict['select'][i] = ".".join(l)
            else: #说明是个列
                #看看列的属性
                if Table[l[1]] == 'number':
                    l[-1] = 'sum'
                else:
                    l[-1] = 'count'
                predict['select'][i] = ".".join(l)
    #再来处理orderby
    for i in range(len(predict['orderby'])):
        if predict['orderby'][i] == []:return predict
        l = predict['orderby'][i][0].split('.')
        if l[-1] == 'count' or l[-1] == 'sum':
            if len(l) == 2: #说明就是表
                l[-1] = 'count'
                predict['orderby'][i][0] = ".".join(l)
            else: #说明是个列
                #看看列的属性
                if Table[l[1]] == 'number':
                    l[-1] = 'sum'
                else:
                    l[-1] = 'count'
                predict['orderby'][i][0] = ".".join(l)

    #处理where
    where = []
    for i in range(len(predict['where'])):
        for key,value in predict['where'][i].items():
            dic = {}
            l = key.split('.')
            if l[-1] == 'count' or l[-1] == 'sum':
                if len(l) == 2:  # 说明就是表
                    l[-1] = 'count'
                    dic[".".join(l)] = value
                else:
                    if Table[l[1]] == 'number':
                        l[-1] = 'sum'
                    else:
                        l[-1] = 'count'
                    dic[".".join(l)] = value
            else:
                dic[key] = value
            where.append(dic)
    predict['where'] = where
    return predict



def remove_select_where(predict):
    #先找出where中的东西
    new_predict = {}
    new_predict['where'] = predict['where']
    new_predict['orderby'] = predict['orderby']
    new_predict['groupby'] = predict['groupby']
    new_predict['select'] = []
    v = []
    for i in range(len(predict['where'])):
        for key,value in predict['where'][i].items():
            if value[0] == 'min' or value[0] == 'max':
                v.append(key)
    for j in range(len(predict['select'])):
        if predict['select'][j] not in v:
            new_predict['select'].append(predict['select'][j])
    return new_predict

import copy
def compare(predict, true, key):
    #res = {'From':[],'Select':[],'Where':[],'orderby':[],'groupby':[]}
    #先把true里面的count(*)去掉
    true_sql = copy.copy(true)
    try:
        true_sql = clear(true_sql)
        #处理下count 和 sum 问题
    except:
        print(true_sql)
        print(key)
        exit(100)

    #类型搞成一致, 起什么名字呢
    predict = type_consistent(predict)

    #统一下类型 列为number的是sum, 列为string, date, 或者是表的为count, 在select和orderby中
    predict = sum_count_transform(predict)

    #在select中把where的东西去掉
    #predict = remove_select_where(predict)
    #predict = putPatch(predict)
    if predict['select'] == []:predict['select'].append(t_name)

    select = compareList(predict['select'], true_sql['select'])
    #orderby = compareList(predict['orderby'], true_sql['orderby'])
    groupby = compareList(predict['groupby'], true_sql['groupby'])
    where = compareDict(predict['where'],true_sql['where'])
    if select and groupby and where:
        return True,predict
    else:
        return False,predict


def output_content(result,abs):
    #文件名
    file_name = result[0]['utterance']
    #文件夹, 叫什么呢？？
    dir_name = 'featureDir'
    if not os.path.exists(dir_name): os.mkdir(dir_name)
    file_name = re.sub("[\.\!\/_,:$%^*?(+\"\']+|[+——！，。？、~@#￥%……&*（）]", "", file_name)
    fw = open(os.path.join(dir_name,str(file_name)),'w',encoding='utf-8')
    fw.write('utterance : {0}'.format(abs)+'\n')
    for result_index in range(len(result)):
        content = result[result_index]
        for i in range(len(content['content'])):
            pattern , scope = content['content'][i]
            fw.write("pattern : {0}, scope : {1}".format(pattern,scope)+'\n')
        fw.write("label : {0}".format(content['label'])+'\n\n')



def generate_data(dic,length,key,abs,true_sql):
    global res
    global s
    new_node = postprocessing(dic, length)
    output_file = open(os.path.join('output',key),'a',encoding='utf-8')
    result = []
    analysis = False
    all_correct = True
    for root in new_node:
        flag = False
        assert root.val.value == 'T'
        init()
        dic = {}
        if type(root.val) == TClass:
            res['select'].append(t_name)
        else:
            s = ""
            dfs(root.val,key)
            output_file.write(s+'\n')
            iteration(root.val, key)

        if res['select'] == [] and res['where'] == []: res['select'].append(t_name)

        arg1, arg2 = compare(res, true_sql, key)
        if arg1 == True:
            flag = True
        content = generateRule(root,abs)
        if content == []:
            print(key)
            #exit(300)
            continue
        dic['content'] = content
        if flag == True:
            analysis = True
            dic['label'] = 1
        else:
            all_correct = False
            dic['label'] = 0
        dic['utterance'] = key
        result.append(dic)
    if len(result) > 0:
        output_content(result, abs)
    if analysis == True and all_correct == False:
        return result
    else: return []

