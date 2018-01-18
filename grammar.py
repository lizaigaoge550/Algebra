class Grammar(object):

    def __init__(self):
        self._rule = []
        self._grammar = []

    def read(self,path):
        for line in open(path).readlines():
            line = line.strip()
            if len(line.split('#')) == 2:
                lhs,rhs = line.split('#')
                item = (rhs,lhs,None)
            else:
                try:
                    lhs,rhs,func = line.split('#')
                except:
                    print("line " , line)
                    exit(0)
                item = (rhs,lhs,func)
            self._grammar.append(item)

    def rule(self):
        return self._rule

    def grammar(self):
        return self._grammar






