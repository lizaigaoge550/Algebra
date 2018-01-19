from opt_class import  Modify, Max,Min,Avg,Count,Sum
import re
import numpy as np

def check(node):
    if type(node) == Max or type(node) == Min or type(node) == Avg or type(node) == Count or type(node) == Sum:
        return type(node).__name__.lower()
    else:
        return node.value


#这版已经没argmax 和 argmin了 多了 blank 和 excluding
def pre_order(root):
    global l
    #首先写入根节点信息
    if root == None: return
    if root.lchild and root.rchild:
        pattern = check(root.val) + ":" + check(root.lchild.val) +"#"+ check(root.rchild.val)
        span = "(" + str(root.start)+','+str(root.end) + ")" + ":" + "(" + str(root.lchild.start)+','+str(root.lchild.end) + ")"+\
               " "+"(" + str(root.rchild.start)+','+str(root.rchild.end) + ")"
        #fw.write(pattern+'\t'+span+'\n')
        l.append(pattern+'\t'+span)
    elif root.lchild:
        pattern = check(root.val) + ":" + check(root.lchild.val)
        span = "(" + str(root.start) + ',' + str(root.end) + ")" + ":" + "(" + str(root.lchild.start) + ',' + str(
            root.lchild.end) + ")"
        #fw.write(pattern + '\t' + span+'\n')
        l.append(pattern+'\t'+span)
    elif root.rchild:
        pattern = check(root.val) + ":" + check(root.rchild.val)
        span = "(" + str(root.start) + ',' + str(root.end) + ")" + ":" + "(" + str(root.rchild.start) + ',' + str(
            root.rchild.end) + ")"
        #fw.write(pattern + '\t' + span+'\n')
        l.append(pattern+'\t'+span)
    pre_order(root.lchild)
    pre_order(root.rchild)



def expandSpan(left,right,utterance,scope):
    #找到前一个tag
    flagStart = False;flagStartTrunc = False
    flagEnd = False;flagEndTrunc = False
    if left > 0:
        for start in range(left-1,-1,-1):
            flagStart = True
            if utterance[start] == 'c' or utterance[start] == 'v' or utterance[start] == 'N' or utterance[start] == 'T' \
                    or utterance[start] == 'D' or utterance[start] == 'blank' \
                or utterance[start] == 'Excluding':
                flagStartTrunc = True
                break
        if flagStartTrunc == True:
            start += 1


    if right < len(utterance)-1:
        for end in range(right+1,len(utterance)):
            flagEnd = True
            if utterance[end] == 'c' or utterance[end] == 'v' or utterance[end] == 'N' or utterance[
                end] == 'T' or utterance[end] == 'D' or utterance[end] == 'blank' \
                    or utterance[end] == 'Excluding':
                flagEndTrunc = True
                break
        if flagEndTrunc == False:
            end += 1

    if flagStart == True and flagEnd == True:
        return utterance[start:end]
    elif flagStart == True:
        return utterance[start:right+1]
    elif flagEnd == True:
        return utterance[left:end]
    else:
        return scope



def extractFeatures(root,l,r):
    def extract(node): #lambda(F).T
        fea = np.array([0, 0, 0])
        if 'lambda' in node:
            arg, express = node.split(".")
            arg = re.search('\(.*\)', arg).group()[1:-1].split(',')
            if 'c' in arg: fea[0] = 1
            if 'F' in arg: fea[1] = 1
            if 'T' in arg: fea[2] = 1
        return fea
    f1 = extract(root)
    f2 = extract(l)
    f3 = extract(r)
    f = np.concatenate((f1,f2,f3))
    return f

def extractPattern(rootspan,lchildspan,rchildspan,root,lchild, rchild, utterance):
    p = []
    rootscope = re.search('\(.*\)', rootspan).group()[1:-1].split(',')
    rootscope = np.arange(int(rootscope[0]),int(rootscope[1])+1)

    lchildscope = re.search('\(.*\)', lchildspan).group()[1:-1].split(',')
    lchildscope = np.arange(int(lchildscope[0]), int(lchildscope[1]) + 1)
    if len(lchildscope) == 1 and lchild in ['c','V','N','D','T','blank','Excluding']:  #不是typerising
        p.append(utterance[lchildscope[0]])
    else:
        p.append(lchild)


    rchildscope = re.search('\(.*\)', rchildspan).group()[1:-1].split(',')
    rchildscope = np.arange(int(rchildscope[0]), int(rchildscope[1]) + 1)

    subscope = np.concatenate((lchildscope,rchildscope))
    for i in range(len(rootscope)):
        if rootscope[i] not in subscope:
            try:
                p.append(utterance[rootscope[i]])
            except Exception as e:
                print(e)
                print(utterance)
                print(rootscope)
                exit(20000)

    if len(rchildscope) == 1 and rchild in ['c','V','N','D','T','blank','Excluding']:
        try:
            p.append(utterance[rchildscope[0]])
        except Exception as e:
            print(e)
            print(rchildscope)
            print(utterance)
            exit(20000)
    else:
        p.append(rchild)
    return root+':'+",".join(p)

def removeLambda(node):
    if 'lambda' in node:
        node = node.split('.')[-1]
    return node

def post_processing(utterance):
    global l
    utterance = utterance.split()
    rl = []
    for i in range(len(l)):
        #average c of T by c
        #T:F,lambda(F).T  (0,5):(0,1)(3,5) --> T:F,T (0,0,0,0,1,0), T:F,of,T , [average,c,of,T,by,c]
        #F:lambda(c).F,c  (0,1):(0,0)(1,1) --> F:F,c (0,0,0,1,0,0), F:average,c, F: average c, [average,c]
        #lambda(F).T:T,lambda(F).G (3,5):(3,3)(4,5) --> F:T,G (0,1,0,0,0,1), T:T,G, [T,by,c]
        #lambda(F).G:lambda(F,c).G,c (4,5):(4,4)(5,5) --> G:G,c (0,1,1,1,0,0) G:by c [by,c]

        pattern, span = l[i].split('\t')
        rootspan, lhsspan = span.split(':')  # (0,5) (0,1)(3,5)
        root, child = pattern.split(':') #T  F, lambda(F).T
        left, right = re.search('\(.*\)', rootspan).group()[1:-1].split(',')
        left = int(left)
        right = int(right)
        scope = utterance[left:right + 1]
        if scope == []:
            print(utterance)
            raise("scope is None")
        if '#' not in child: #type-rasing的情况

            if left == right:
                #扩充scope
                if 'max' in pattern or 'min' in pattern or 'avg' in pattern or 'sum' in pattern or 'count'in pattern:
                    scope = expandSpan(left,right,utterance,scope)
                rl.append([pattern, scope])

        else:
            lchild, rchild = child.split('#')#F,  lambda(F)
            # 新的pattern
            root = removeLambda(root)
            lchild = removeLambda(lchild)
            rchild = removeLambda(rchild)
            newpattern = root+':'+lchild+','+rchild
            rl.append([newpattern,scope])
    return rl

l = []
ab = []
def extract_abstact_data(root):
    if root == None:return
    if root.lchild == None and root.rchild == None:
        #leaf node
        if root.val.value == 'V':
            ab.append(('v',(root.start,root.end)))
        else:
            ab.append((root.val.value,(root.start,root.end)))
        return
    extract_abstact_data(root.lchild)
    extract_abstact_data(root.rchild)

#处理c和T的问题
def new_abstract_data(abstract_data):
    global ab
    abstract_data = abstract_data.split()
    for abstract_data_index in range(len(abstract_data)):
        for ab_index in range(len(ab)):
            start, end = ab[ab_index][1]
            if start == end and abstract_data_index == start:
                if ab[ab_index][0] == 'c' or ab[ab_index][0] == 'T':
                    abstract_data[abstract_data_index] = ab[ab_index][0]
    return " ".join(abstract_data)

def generateRule(root,abstract_data):
    global l, ab
    l = []
    ab  = []
    #pre_order
    pre_order(root)
    #重新提取abstract_data
    extract_abstact_data(root)
    abstract_data = new_abstract_data(abstract_data)

    return post_processing(abstract_data)

        #fw.write('\n')