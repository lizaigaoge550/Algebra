from opt_class import *
from class_file import *
from node import Node



def generate_test_root_1():
    # f -> f(c)
    f = Avg('shark_attack','age','number')
    c = cClass(t_name='shark_attack',c_name='age',c_type='number',value='shark_attack.age')
    f.param.val = c
    f.value = 'F'
    node6 = Node(None,None,f)


    #filter
    filter = In('shark_attck','activity','string')
    c =  cClass(t_name='shark_attack',c_name='activity',c_type='string',value='shark_attack.activity')
    v = VClass(t_name='shark_attack',c_name='activity',c_type='string',value='shark_attack.activity.swimming')
    filter.param_1.val = c
    filter.param_2.val = v
    filter.value = 'Filter'
    node7 = Node(None,None,filter)


    #node4
    f_1 = Modify('shark_attack',c_name='age',c_type='number')
    f_1.param_1.val = f
    f_1.param_2.val = filter
    f_1.value = 'F'
    node4 = Node(node6,node7,f_1)


    #node5 N
    n = NClass('shark_attck',None,'number','>1000')
    node5 = Node(None,None,n)

    # node2 In -> f,N
    filter_1 = In('shark_attack', 'age', 'number')
    filter_1.param_1.val = f_1
    filter_1.param_2.val = n
    filter_1.value = 'Filter'
    node2 = Node(node4,node5,filter_1)

    # node1 : filter t --> t
    t = Select('shark_attack', ['age', 'activity'], ['number', 'string'])

    #T
    T = TClass('shark_attack',['age','activity'],['number','string'])

    node3 = Node(None,None,T)
    t.param_1.val = filter_1
    t.param_2.val = T
    t.value = 'T'
    node1 = Node(node2,node3,t)

    return node1

def generate_test_tree_2():
    c = cClass(t_name='shark_attack', c_name='age', c_type='number', value='shark_attack.age')
    #node5 = Node(None,None,c)


    filter = In('shark_attck', 'activity', 'string')
    c_1 = cClass(t_name='shark_attack', c_name='activity', c_type='string', value='shark_attack.activity')
    v = VClass(t_name='shark_attack', c_name='activity', c_type='string', value='shark_attack.activity.swimming')
    filter.param_1.val = c_1
    filter.param_2.val = v
    filter.value = 'Filter'
    node5 = Node(None, None, filter)

    f = Avg('shark_attack', 'age', 'number')
    #c = cClass(t_name='shark_attack', c_name='age', c_type='number', value='shark_attack.age')
    f.param.val = c
    f.value = 'F'
    node4 = Node(None,None,f)

    # node3 N
    n = NClass('shark_attck', None, 'number', '>1000')
    node3 = Node(None,None,n)

    #node2 nodify-->(f,n)
    f_2 = Modify(t_name='shark_attack', c_name='age', c_type='number')
    f_2.value = 'F'
    f_2.param_1.val = f
    f_2.param_2.val = filter
    node2 = Node(None,None,f_2)

    filter_1 = In(t_name='shark_attack', c_name='age', c_type='number')
    filter_1.value = 'Filter'
    filter_1.param_1.val = f_2
    filter_1.param_2.val = n
    node1 = Node(None,None,filter_1)

    # T
    pro = Project(t_name='shark_attack', c_name='age', c_type='number')
    pro.value = 'T'
    T = TClass('shark_attack', ['age', 'activity'], ['number', 'string'])
    pro.param_1.val = T
    pro.param_2.val = filter_1
    node0 = Node(None,None,pro)

    return node0