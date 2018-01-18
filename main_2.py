#coding=utf-8
from parser_algorithm import bottom_up_parser
from grammar import Grammar
from node import Node
from type_raising import type_rasing
from read_data_v3 import read_data
import re
import pickle
import numpy as np

from expression import generate_expression, generate_dict,generate_data

def get_leaf_logical(leaf,gDict,key,i,j):
    #对这个leaf做type-raising
    nodelist = [Node(None,None,leaf,i,j)]
    return type_rasing(gDict,nodelist,i,j,key)



def get_non_terminal_logical(dic,start,end,gDict,key):
    assert end > start
    for p in range(start,end):
        if len(dic[start][p]) > 0 and len(dic[p+1][end]) > 0:
            #遍历dic[i][p] 和 dic[p+1][j] 中的每个元素
            for i in range(len(dic[start][p])):
                for j in range(len(dic[p+1][end])):
                    g = bottom_up_parser(dic[start][p][i], dic[p+1][end][j], gDict,key)
                    dic[start][end] += g

def run_batch(input,gDict,sql,abs):
    log = {}
    final = []
    for key,v in input.items():
        n = len(v)
        dic = [[[] for _ in range(n)] for _ in range(n)]
        for length in range(n):  # length --> 0,1,2,3,4
            for i in range(n - length):
                j = length + i
                if i == j:
                    for k in range(len(v[i])):
                        g = get_leaf_logical(v[i][k][0], gDict,key,v[i][k][1],v[i][k][2])
                        dic[i][j] += g
                else:
                    get_non_terminal_logical(dic, i, j, gDict,key)
        #key = re.sub("[\.\!\/_,$%^*?(+\"\']+|[+——！，。？、~@#￥%……&*（）]", "",key)
        # #打印每层的node: value:class
        # fw = open('log','w')
        # for i in range(n):
        #     for j in range(n):
        #         fw.write("start:{0}, end:{1}\n".format(i,j))
        #         for k in range(len(dic[i][j])):
        #             fw.write(dic[i][j][k].val.value+":"+type(dic[i][j][k].val).__name__+'\n')

        #c = generate_expression(dic, n - 1, key)
        generate_dict(dic,n-1,key,sql[key])
        #r = generate_data(dic, n-1, key, abs[key], sql[key])
    #     if r == []:
    #         #print(r)
    #         pass
    #     else:
    #         final.append(r)
    #         print(r)
    # print(len(final))
    # pickle.dump(final, open('shark_data.pkl', 'wb'))
    #     if c > 0:
    #       log[key] = c
    # #最大长度
    # max_len = max(list(log.values()))
    # # 最小长度
    # min_len = min(list(log.values()))
    # # 平均长度
    # avg_len = np.mean(list(log.values()))
    # print("max_len : {0}, min_len : {1}, avg_len : {2}".format(max_len, min_len, avg_len))
    # #输出长度超过100 的 utterance
    # fw = open('more than 100', 'w')
    # for k, v in log.items():
    #     if v >= 100: fw.write(k + ":" + str(v)+'\n')
    # fw.close()

#max_len : 578, min_len : 1, avg_len : 17.889204545454547
if __name__ == '__main__':
    grammar = Grammar()
    grammar.read('new_grammar')
    gDict = grammar.grammar()
    #input,sql = read_data('SharkAttack')
    #input, sql = read_data("D:\\Algebra_fuben_new_grammar\\SharkAttack")
    #input,sql,abs = read_data('SharkAttackTestDir_v2')
    input,sql,abs = read_data('jobs_data_post')

    run_batch(input,gDict,sql,abs)