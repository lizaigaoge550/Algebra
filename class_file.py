#coding=utf-8

class BaseClass(object):
    def __init__(self, t_name, c_name, c_type):
        self.t_name = t_name
        self.c_name = c_name
        self.c_type = c_type

class cClass(BaseClass):
    def __init__(self,t_name, c_name, c_type, value):
        super(cClass,self).__init__(t_name, c_name, c_type)
        self.value = 'c'
        self.description = value
    def __str__(self):
        return 'c'

class TClass(BaseClass):
    def __init__(self, t_name, c_name, c_type):
        super(TClass,self).__init__(t_name,c_name,c_type)
        self.description = t_name
        self.value = 'T'
    def __str__(self):
        return 'T'



class VClass(BaseClass):
    def __init__(self,t_name, c_name, c_type, value):
        super(VClass,self).__init__(t_name,c_name,c_type)
        self.value = 'V'
        self.description = value
    def __str__(self):
        return 'V'


class NClass(BaseClass):
    def __init__(self,t_name,c_name,c_type,value):
        super(NClass,self).__init__(t_name,c_name,c_type)
        self.c_type = 'number' #N 的 type一定是number
        self.value = 'N'
        self.description = value
    def __str__(self):
        return 'N'

class DClass(BaseClass):
    def __init__(self,t_name,c_name,c_type, value):
        super(DClass,self).__init__(t_name,c_name,c_type)
        self.c_type = 'date' #D 的 type一定是number
        self.value = 'D'
        self.description = value
    def __str__(self):
        return 'D'

class Dir(BaseClass):
    def __init__(self,t_name,c_name,c_type, dir='asc'):
        super(Dir, self).__init__(t_name, c_name, c_type)
        self.value = 'dir'
        self.description = dir
    def __str__(self):
        return 'dir'

class BlankClass(BaseClass):
    def __init__(self,t_name,c_name,c_type,value):
        super(BlankClass,self).__init__(t_name,c_name,c_type)
        self.c_type = 'blank' #N 的 type一定是number
        self.value = 'blank'
        self.description = value
    def __str__(self):
        return 'blank'

class ExcludeClass(BaseClass):
    def __init__(self,t_name,c_name,c_type,value):
        super(ExcludeClass,self).__init__(t_name,c_name,c_type)
        self.c_type = "Excluding" #N 的 type一定是number
        self.value = 'Excluding'
        self.description = value
    def __str__(self):
        return 'Excluding'



