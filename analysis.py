#coding=utf-8
from opt_class import *
def to_sql(g,res):
    #用来解析In (G,N)
    #分成两种情况
    # G.f 是 aggerate
    #遍历参数找到f 和 c
    f = None
    c = None
    if g.param_1.val.value == 'F':
        f = g.param_1.val
        c = g.param_2.val
    else:
        f = g.param_2.val
        c = g.param_1.val

    #先把c加到groupby中
    if  c.description in res['groupby']:
        raise ('In(G,N)) group is not valid')
    res['groupby'].append(c.description)

    #c添加到select里面
    if c.description in res['Select']:
        raise ('In(G,N) c is not valid')
    res['Select'].append(c.description)

    #f 是 aggregate
    #将 f 添加到 select 和 where 中
    if type(f) == Sum or type(f) == Max or type(f) == Min or type(f) == Avg or type(f) == Count:
        value = f.param.description + '.' + type(f).__name__
        if value in res['Select']:
            raise ("In(G,N) F is not valid")
        res['Select'].append(value)

        for i in range(len(res['Where'])):
            if value in res['Where'][i]:
                res['Where'][i][value].append('numberrange')
            else:
                res['Where'][i][value] = ['numberrange']

    #f 是 argmax 和 argmin where 添加 (f.f)
    elif type(f) == Argmax or type(f) == Argmin:
        #对应3个操作
        ff = f.val
        if type(ff.val) == Sum or type(ff.val) == Max or type(ff.val) == Min or \
                type(ff.val) == Avg or type(ff.val) == Count:
            value = ff.param.description + '.' + type(ff).__name__




