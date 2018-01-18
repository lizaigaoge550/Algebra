import glob
import os
import json
from opt_class import *
from class_file import *
from utils import get_opt

from getTable import get_table

import copy
#t_name = 'shark_attack'
# t_name = 'job'
# #Table = {"country":'string', 'gender':'string', 'fatality':'string','activity':'string','attack':'number','year':'date', 'count(t)':'number'}
# Table = {'field':'string','title':'string', 'posting_date':'date', 'desired_year_experience':'number',
#          'required_academic_qualification':'string','company':'string','area':'string',
#          'city':'string','country':'string','programming_language':'string','salary':'number','plantform':'string','count(t)':'number'
#          }
t_name,Table = get_table()


def generate_index(inital,s,count):
    if count == 0:
        s.append(copy.copy(inital))
        return
    for i in range(2):
        inital.append(i)
        generate_index(inital,s,count-1)
        del inital[-1]


def no_pat(tag,index):
    s = []
    for i in range(len(tag[index])):
        if tag[index][i] != 'pat':
            s.append(tag[index][i])
    return s

def generate_multi_tags(tag):
    #tag中可能有pat所以要拆分
    #获取pat的索引
    pat_index = []
    index_count = 0
    for tag_index in range(len(tag)):
        if 'pat' in tag[tag_index]:
            pat_index.append(tag_index)
            index_count += 1
    #产生索引
    s = []
    generate_index([],s,index_count)
    data = []

    for s_index in range(len(s)):
        tag_copy = copy.copy(tag)
        for index,value in zip(pat_index,s[s_index]):
            if value == 0:
                tag_copy[index] = []
            else:
                tag_copy[index] = no_pat(tag_copy,index)
        data.append(tag_copy)
    return data





def read_data(path):
    data = {}
    sql = {}
    abstract_data = {}
    for eachfile in glob.glob(os.path.join(path,'*')):
        # try:
        #     item = json.load(open(eachfile,encoding='utf-8'))
        # except Exception as e:
        #     print(eachfile)
        #     print(e)
        item = json.load(open(eachfile,encoding='utf-8-sig'))
        # 拿出tag
        utterance = item['new_tag_utterance']

        #取出原来的utterance
        raw_utterance = item['raw_utterance'].split()

        tags = []
        for i in range(len(utterance)):
            tag = utterance[i]['tags']  # 是一个list
            left = utterance[i]['left_index']
            right = utterance[i]['right_index']
            flag = False  # 防止出现两个sum
            label = []
            for j in range(len(tag)):
                # 首先提取type
                value = tag[j]['Type']
                if value == 'Vistype': continue
                # #如果value 是 c 和 V, T 的话
                if value == 'c' or value == 'v' or value == 'T' or value == 'N' or value == 'D' or value == 'Blank' or value == 'Excluding':
                    try:
                        description = tag[j]['value'].split('-')[0]
                    except:
                        print(eachfile)
                        exit(1000)
                    # v_description =
                    if value == 'c' or value == 'v':
                        c_name = description.split('.')[1]
                        if c_name not in Table: print(c_name); print(c_name);raise ("c_name not in Table")
                        if value == 'c':

                            label.append([cClass(t_name=t_name, c_name=c_name, c_type=Table[c_name], value=description),left,right])


                        if value == 'v':
                            label.append([VClass(t_name=t_name, c_name=c_name, c_type=Table[c_name],
                                                value=tag[j]['value']),left,right])

                    elif value == 'T':
                        label.append(
                            [TClass(t_name=t_name, c_name=list(Table.keys()), c_type=list(Table.values())),left,right])
                    elif value == 'N':
                        label.append([NClass(None, None, 'string', tag[j]['value']),left,right])
                    elif value == 'D':
                        label.append([DClass(t_name=t_name, c_name=tag[j]['col'].split('.')[-1], c_type='date', value=tag[j]['value']),
                                      left,right])
                    elif value == 'Blank':
                        f = BlankClass(None, None, None, 'blank')
                        label.append([f,left,right])
                    elif value == 'Excluding':
                        f = ExcludeClass(None, None, None, 'Excluding')
                        label.append([f,left,right])
                    else:
                        print(value)
                        raise ('Type is not right')
                else:
                    func = value.split('.')[-1]  # 有F.G, F.min..., F.argmax, F.count-c(等价于F,sum), F.count-t(F:count(T)), Dir.dsc, F.order
                    if func == 'G':
                        try:
                            if 'EachFilter' in tag[j]['values']: continue
                        except:
                            print(tag)
                            print(eachfile)
                            exit(2000)
                        if 'C' in tag[j]['values']: continue
                        g = Group(None, None, None)
                        g.value = 'lambda(F,c).G'
                        try:
                            label.append([g,left,right])
                        except:
                            print(eachfile)
                            exit(100)
                    elif func == 'min' or func == 'max' or func == 'avg':
                        f = get_opt(func)
                        f.value = 'lambda(c).F'
                        label.append([f,left,right])
                    elif func == 'sum':
                        if flag == False:
                            f = get_opt(func)
                            f.value = 'lambda(c).F'
                            flag = True
                            label.append([f,left,right])
                    elif func == 'argmin' or func == 'argmax':
                        f = get_opt(func)
                        if 'EachFilter' in tag[j]['values']:
                            f.value = 'lambda(F,EachFilter).F'
                        else:
                            f.value = 'lambda(F,c).F'
                        label.append([f,left,right])
                    elif func == 'count-c':
                        if flag == False:
                            f = Count(None, None, None)
                            f.value = 'lambda(c).F'
                            flag = True
                            label.append([f,left,right])
                    elif func == 'count-t':
                        f = Count(None, None, None)
                        f.value = 'lambda(T).F'

                        label.append([f,left,right])
                    elif func == 'order':
                        f = Order(None, None, None)
                        f.value = 'lambda(c,T,dir).T'
                        label.append([f,left,right])
                    elif func == 'dsc':
                        f = Dir(None, None, None, func)
                        label.append([f,left,right])
                    elif func == 'pat':
                        continue

                    else:
                        print(value)
                        print(eachfile)
                        raise ('Type is not right')
            if len(label): tags.append(label)
        if len(tags) == 0: print(item);continue
        tags = generate_multi_tags(tags)
        data[item["raw_utterance"]] = tags
        sql[item['raw_utterance']] = item["sql_info"]
        abstract_data[item['raw_utterance']] = item['abstract_utterance']
        # print('id : {0}, len : {1}'.format(id,len(tags)))
        #id += 1
    return data, sql, abstract_data


