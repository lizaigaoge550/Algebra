#coding=utf-8
import json
from opt_class import *
from class_file import *
from utils import get_opt

Table = {"country":'string', 'gender':'string', 'fatality':'string','activity':'string','attack':'number','year':'date'}
def read_data():
    data = {}
    id = 0
    #test_file
    #utterance_tag_sql.txt

    with open('data\\utterance_tag_sql.txt') as fr:
        for line in fr.readlines():
            item = json.loads(line)
            #拿出tag
            utterance = item['new_tag_utterance']
            tags = []
            for i in range(len(utterance)):
                tag = utterance[i]['tags'] #是一个list
                flag = False #防止出现两个sum
                label = []
                for j in range(len(tag)):
                    #首先提取type
                    value = tag[j]['Type']
                    if value == 'Vistype':continue
                    # #如果value 是 c 和 V, T 的话
                    if value == 'c' or value == 'v' or value == 'T' or value == 'N' or value == 'D':
                        description = tag[j]['value'].split('-')[0]
                        #v_description =
                        if value == 'c' or value == 'v':
                            c_name = description.split('.')[1]
                            if c_name not in Table: print(c_name); print(c_name);raise("c_name not in Table")
                            if  value == 'c':
                                #if c_name == 'year':c_type = 'string'
                                #else:c_type = Table[c_name]
                                label.append(cClass(t_name='shark_attack',c_name=c_name,c_type=Table[c_name],value=description))
                            if value == 'v':
                                label.append(VClass(t_name='shark_attack',c_name=c_name,c_type=Table[c_name],value=tag[j]['value']))

                        elif value == 'T':
                            label.append(TClass(t_name='shark_attack',c_name=list(Table.keys()),c_type=list(Table.values())))
                        elif value == 'N':
                            label.append(NClass(None,None,'string',tag[j]['value']))
                        elif value == 'D':
                            label.append(DClass(t_name='shark_attack',c_name='year',c_type='data',value=tag[j]['value']))
                        else:
                            print(value)
                            raise ('Type is not right')
                    else:
                        func = value.split('.')[-1] #有F.G, F.min..., F.argmax, F.count-c(等价于F,sum), F.count-t(F:count(T)), Dir.dsc, F.order
                        if func == 'G':
                            if 'EachFilter' in tag[j]['values']:continue
                            if 'C' in tag[j]['values']:continue
                            g = Group(None,None,None)
                            g.value = 'lambda(F,c).G'
                            label.append(g)
                        elif func == 'min' or func == 'max' or func == 'avg':
                            f = get_opt(func)
                            f.value = 'lambda(c).F'
                            label.append(f)
                        elif func == 'sum':
                            if flag == False:
                                f = get_opt(func)
                                f.value = 'lambda(c).F'
                                flag = True
                                label.append(f)
                        elif func == 'argmin' or func == 'argmax':
                            f = get_opt(func)
                            f.value = 'lambda(F,c).F'
                            label.append(f)
                        elif func == 'count-c':
                            if flag == False:
                                f = Sum(None,None,None)
                                f.value = 'lambda(c).F'
                                flag = True
                                label.append(f)
                        elif func == 'count-t':
                            f = Count(None,None,None)
                            f.c_type = 'number'
                            f.c_name = list(Table.keys())
                            f.t_name = 'shark_attack'
                            #f.description = '*'
                            f.param.val = TClass(t_name='shark_attack',c_name=list(Table.keys()),c_type='number')
                            f.value = 'F'

                            label.append(f)
                        elif func == 'order':
                            f = Order(None,None,None)
                            f.value = 'lambda(c,T,dir).T'
                            label.append(f)
                        elif func == 'dsc':
                            f = Dir(None,None,None,func)
                            label.append(f)
                        else:
                            print(value)
                            raise('Type is not right')
                if len(label):tags.append(label)
            if len(tags) == 0:print(item);continue
            data[item["raw_utterance"]] = tags
            #print('id : {0}, len : {1}'.format(id,len(tags)))
            id += 1
    return data