import glob
import os
import json
from opt_class import *
from class_file import *
from utils import get_opt

#Table = {"country":'string', 'gender':'string', 'fatality':'string','activity':'string','attack':'number','year':'date', 'count(t)':'number'}
# Table = {'field':'string','title':'string', 'posting_date':'date', 'desired_year_experience':'number',
#          'required_academic_qualification':'string','company':'string','area':'string',
#          'city':'string','country':'string','programming_language':'string','salary':'number','plantform':'string','count(t)':'number'
#          }
'''
field	
title	
posting_date
desired_year_experience	
required_academic_qualification	
company	
area	
city	
country	
programming_language	
salary	
plantform 
'''
#t_name = 'job'
t_name = 'shark_attack'
def read_data(path):
    data = {}
    sql = {}
    for eachfile in glob.glob(os.path.join(path,'*')):
        try:
             item = json.load(open(eachfile,encoding='utf-8-sig'))
        except Exception as e:
            print(eachfile)
            print(e)
            exit(100)
        #item = json.load(open(eachfile,encoding='utf-8'))
        # 拿出tag
        utterance = item['new_tag_utterance']
        tags = []
        for i in range(len(utterance)):
            tag = utterance[i]['tags']  # 是一个list
            flag = False  # 防止出现两个sum
            label = []
            for j in range(len(tag)):
                # 首先提取type
                value = tag[j]['Type']
                if value == 'Vistype': continue
                # #如果value 是 c 和 V, T 的话
                if value == 'c' or value == 'v' or value == 'T' or value == 'N' or value == 'D':
                    try:
                        description = tag[j]['value'].split('-')[0]
                    except:
                        print(eachfile)
                        print(tag[j])
                        exit(1000)
                    # v_description =
                    if value == 'c' or value == 'v':
                        c_name = description.split('.')[1]
                        if c_name not in Table: print(c_name); print(c_name);raise ("c_name not in Table")
                        if value == 'c':
                            # if c_name == 'year':
                            #     c_type = 'string'
                            # else:
                            #     c_type = Table[c_name]
                            label.append(cClass(t_name=t_name, c_name=c_name, c_type=Table[c_name], value=description))
                        if value == 'v':
                            label.append(VClass(t_name=t_name, c_name=c_name, c_type=Table[c_name],
                                                value=tag[j]['value']))

                    elif value == 'T':
                        label.append(
                            TClass(t_name=t_name, c_name=list(Table.keys()), c_type=list(Table.values())))
                    elif value == 'N':
                        label.append(NClass(None, None, 'number', tag[j]['value']))
                    elif value == 'D':
                        label.append(DClass(t_name=t_name, c_name=tag[j]['col'].split('.')[-1], c_type='date', value=tag[j]['value']))
                    else:
                        print(value)
                        raise ('Type is not right')
                else:
                    func = value.split('.')[
                        -1]  # 有F.G, F.min..., F.argmax, F.count-c(等价于F,sum), F.count-t(F:count(T)), Dir.dsc, F.order
                    if func == 'G':
                        if 'EachFilter' in tag[j]['values']: continue
                        if 'C' in tag[j]['values']: continue
                        g = Group(None, None, None)
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
                    elif func == 'count-c':
                        if flag == False:
                            f = Count(None, None, None)
                            f.value = 'lambda(c).F'
                            flag = True
                            label.append(f)
                    elif func == 'count-t':
                        f = Count(None, None, None)
                        #f.c_type = 'number'
                        #f.c_name = list(Table.keys())
                        #f.t_name = 'shark_attack'
                        # f.description = '*'
                        #f.param.val = TClass(t_name='shark_attack', c_name=list(Table.keys()), c_type='number')
                        f.value = 'lambda(T).F'

                        label.append(f)
                    elif func == 'order':
                        f = Order(None, None, None)
                        f.value = 'lambda(c,T,dir).T'
                        label.append(f)
                    elif func == 'dsc':
                        f = Dir(None, None, None, func)
                        label.append(f)
                    elif func == 'pat':
                        continue
                    elif func == 'Blank':
                        f = BlankClass(None,None,None,'blank')
                        label.append(f)
                    elif func == 'Excluding':
                        f = ExcludeClass(None,None,None,'Excluding')
                        label.append(f)
                    else:
                        print(value)
                        print(eachfile)
                        raise ('Type is not right')
            if len(label): tags.append(label)
        if len(tags) == 0: print(item);continue
        data[item["raw_utterance"]] = tags
        sql[item['raw_utterance']] = item["sql_info"]
        # print('id : {0}, len : {1}'.format(id,len(tags)))
        #id += 1
    return data, sql
#read_data('SharkAttack')

