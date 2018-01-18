#coding=utf-8
from class_file import BaseClass,Dir


class Parameter(object):
    def __init__(self,name,val):
        self.name = name
        self.val = val



class OptBaseClass(object):
    def __init__(self):
        self.param_1 = Parameter('param_1',None)
        self.param_2 = Parameter('param_2',None)
        self.value = None
        self.description = None
        #self.__dict__.update([self.param_1,self.param_2])



class Project(BaseClass,OptBaseClass): #Project(C,T) Project(c,T) Project(G,T) Project(F,T)
    def __init__(self,t_name, c_name, c_type):
        BaseClass.__init__(self,t_name,c_name,c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1,self.param_2]
        #Proself.__dict__.update(self.param_list)



class Modify(BaseClass,OptBaseClass):
    def __init__(self,t_name, c_name, c_type):
        BaseClass.__init__(self,t_name,c_name,c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1,self.param_2]


class In(BaseClass,OptBaseClass):
    # In(c,N) c.c_type = N.c_type
    # In(F,N) F.c_type = N.c_type
    #In(c,V) c.c_name = V.c_name
    def __init__(self,t_name, c_name, c_type):
        BaseClass.__init__(self,t_name, c_name, c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1,self.param_2]

class Combine(BaseClass,OptBaseClass):
    def __init__(self,t_name, c_name, c_type):
        BaseClass.__init__(self,t_name, c_name, c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1,self.param_2]



class Argmax(BaseClass,OptBaseClass):
    def __init__(self,t_name, c_name, c_type):
        BaseClass.__init__(self,t_name, c_name, c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1,self.param_2]

class Argmin(BaseClass,OptBaseClass):
    def __init__(self,t_name, c_name, c_type):
        BaseClass.__init__(self,t_name, c_name, c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1,self.param_2]


class Select(BaseClass,OptBaseClass): #Select(Filter, T)
    def __init__(self,t_name, c_name, c_type):
        BaseClass.__init__(self,t_name, c_name, c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1,self.param_2]


class Group(BaseClass,OptBaseClass): #Group(F,C|c) Group(F,EachV) Group(G1, C|c)
    def __init__(self,t_name,c_name,c_type):
        BaseClass.__init__(self, t_name, c_name, c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1,self.param_2]

class CombineF(BaseClass,OptBaseClass):
    def __init__(self,t_name,c_name,c_type):
        BaseClass.__init__(self, t_name, c_name, c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1, self.param_2]


class AggrateClass(BaseClass):
    def __init__(self, t_name, c_name, c_type):
        super(AggrateClass,self).__init__(t_name,c_name,c_type)
        self.param = Parameter('param',None)
        self.value = None
        self.param_list = [self.param]
        self.description = None


class Min(AggrateClass):
    def __init__(self, t_name, c_name, c_type):
        super(Min,self).__init__(t_name,c_name,c_type)


class Max(AggrateClass):
    def __init__(self, t_name, c_name, c_type):
        super(Max,self).__init__(t_name,c_name,c_type)

class Avg(AggrateClass):
    def __init__(self, t_name, c_name, c_type):
        super(Avg,self).__init__(t_name,c_name,c_type)

class Sum(AggrateClass):
    def __init__(self, t_name, c_name, c_type):
        super(Sum,self).__init__(t_name,c_name,c_type)

class Count(AggrateClass): #一种参数是一个c类, 一种是一个'*'
    def __init__(self, t_name, c_name, c_type):
        super(Count,self).__init__(t_name,c_name,c_type)
        self.distinct = False

class Order(BaseClass,OptBaseClass):
    def __init__(self,t_name,c_name,c_type):
        BaseClass.__init__(self, t_name, c_name, c_type)
        OptBaseClass.__init__(self)
        self.dir = Dir(None,None,None)
        self.param_list = [self.param_1, self.param_2, self.dir]

class Join(BaseClass,OptBaseClass):
    def __init__(self, t_name, c_name, c_type):
        BaseClass.__init__(self,t_name,c_name,c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1, self.param_2]

class And(BaseClass,OptBaseClass):
    def __init__(self, t_name, c_name, c_type):
        BaseClass.__init__(self, t_name, c_name, c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1, self.param_2]

class Or(BaseClass,OptBaseClass):
    def __init__(self,t_name, c_name, c_type):
        BaseClass.__init__(self, t_name, c_name, c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1, self.param_2]

class Not(BaseClass,OptBaseClass):
    def __init__(self,t_name, c_name, c_type):
        BaseClass.__init__(self,t_name,c_name,c_type)
        OptBaseClass.__init__(self)
        self.param_list = [self.param_1,self.param_2]










