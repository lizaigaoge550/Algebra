from opt_class import *
from class_file import *
#s = Group(t_name='carsale',c_name='sale',c_type='number')
#s.value = "lambda(F).G"
#c = cClass('carsale','sale','number','carsale.sale')
#s.param_1 = c
#v = VClass('carsale','brand','string','carsale.brand.BWM')
#v = VClass('carsale','brand','string','carsale.brand.Toyata')
'''
compare sales of bmw x5 vs toyota x6 by year
Which country total attacks < 3
count of attacks less than 3 for each country
Compare sales of BMW vs Toyota by year
Compare (total) sales of BMW X5 vs Toyota X6 by year 
'''
def example_1():
    '''
    sum of sales of BWM vs Toyata
    '''

    '''sum'''
    f = Sum(None, None, None)
    f.value = 'lambda(c).F'

    '''sales'''
    c = cClass(t_name='carsale', c_name='sale', c_type='number', value='carsale.sale')

    '''BMW'''
    V1 = VClass(t_name='carsale', c_name='brand', c_type='string', value='carsale.brand.BMW')

    '''Toyata'''
    V2 = VClass(t_name='carsale', c_name='brand', c_type='string', value='carsale.brand.Toyata')

    l = [f,c,V1,V2]
    return l

def example_2():
    '''
    average age of customer by type
    '''

    '''average'''
    f = Avg(None, None, None)
    f.value = 'lambda(c).F'

    '''age'''
    c1 = cClass(t_name='customer', c_name='age', c_type='number', value='customer.age')

    '''customer'''
    T = TClass(t_name='customer', c_name=['age', 'type'], c_type=['number', 'string'])

    '''by'''
    G = Group(None, None, None)
    G.value = 'lambda(F,c).G'

    '''type'''
    c2 = cClass(t_name='customer', c_name='type', c_type='string', value='customer.type')
    l = [f,c1,G,c2]
    return l

def example_3():
    '''
    Product which total sales >5000
    '''

    '''product'''
    c1 = cClass(t_name='product', c_name='name', c_type='string', value='product.name')

    '''total'''
    f = Sum(None, None, None)
    f.value = 'lambda(c).F'

    '''sales'''
    c2 = cClass(t_name='product', c_name='sale', c_type='number', value='product.sale')

    '''>5000'''
    n = NClass(t_name=None, c_name=None, c_type=None,value='>5000')

    l = [c1,f,c2,n]

    return l

def example_4():
    '''
    total attack by year in USA
    '''
    '''total'''
    '''average'''
    f = Sum(None, None, None)
    f.value = 'lambda(c).F'

    '''attack'''
    c1 = cClass(t_name='shark', c_name='attack', c_type='number', value='shark.attack')

    '''by'''
    G = Group(None, None, None)
    G.value = 'lambda(F,c).G'

    '''year'''
    c2 = cClass(t_name='shark', c_name='year', c_type='string', value='shark.year')

    '''USA'''
    V = VClass(t_name='shark', c_name='location', c_type='string', value='shark.location.USA')

    l = [f,c1,G,c2,V]

    return l

def example_5():
    '''
    activity that caused the most attacks
    '''

    '''activity'''
    c1 = cClass(t_name='shark', c_name='activity', c_type='string', value='shark.activity')

    '''most'''
    f = Argmax(None,None,None)
    f.value = 'lambda(c,F).F'

    '''attack'''
    c2 = cClass(t_name='shark', c_name='attack', c_type='number', value='shark.attack')

    l = [c1,f,c2]

    return l

def example_6():
    '''
    activity with the least anount of attacks
    '''

    '''activity'''
    c1 = cClass(t_name='shark', c_name='activity', c_type='string', value='shark.activity')

    '''least'''
    f1 = Argmin(None,None,None)
    f1.value = 'lambda(c,F).F'

    '''amount'''
    f2 = Sum(None, None, None)
    f2.value = 'lambda(c).F'

    '''attack'''
    c2 = cClass(t_name='shark', c_name='attack', c_type='number', value='shark.attack')

    l = [c1,f1,f2,c2]

    return l


def example_7():
    '''
    compare sales of bmw x5 vs toyota x6 by year
    '''
    '''sales'''
    c1 = cClass(t_name='carsale', c_name='sale', c_type='number', value='carsale.sale')

    '''bmw'''
    V1 = VClass(t_name='carsale', c_name='brand', c_type='string', value='carsale.brand.BMW')

    '''x5'''
    V2 = VClass(t_name='carsale', c_name='type', c_type='string', value='carsale.type.x5')

    '''toyata'''
    V3 = VClass(t_name='carsale', c_name='brand', c_type='string', value='carsale.brand.Toyata')

    '''x6'''
    V4 = VClass(t_name='carsale', c_name='type', c_type='string', value='carsale.brand.x6')

    '''by'''
    G = Group(None, None, None)
    G.value = 'lambda(F,c).G'

    '''year'''
    c2 = cClass(t_name='carsale', c_name='year', c_type='string', value='carsale.year')

    l = [c1,V1,V2,V3,V4,G,c2]
    return l

def example_8():
    '''
    which country total attack <3
    '''
    '''country'''
    c1 = cClass(t_name='shark', c_name='country', c_type='string', value='shark.country')

    '''total'''
    f = Sum(None, None, None)
    f.value = 'lambda(c).F'

    '''attack'''
    c2 = cClass(t_name='shark', c_name='attack', c_type='number', value='shark.attack')

    '''<3'''
    n = NClass(t_name=None, c_name=None, c_type=None, value='<3')

    return [c1,f,c2,n]

def example_9():
    '''count of attacks less than 3 for each country'''

    '''count'''
    f = Sum(None, None, None)
    f.value = 'lambda(c).F'

    '''attack'''
    c1 = cClass(t_name='shark', c_name='attack', c_type='number', value='shark.attack')

    '''<3'''
    n = NClass(t_name=None, c_name=None, c_type=None, value='<3')

    '''each'''
    G = Group(None, None, None)
    G.value = 'lambda(F,c).G'

    '''country'''
    c2 = cClass(t_name='shark', c_name='country', c_type='string', value='shark.country')

    l = [f,c1,n,G,c2]

    return l

def example_10():
    '''c c T'''
    '''attack'''
    c1 = cClass(t_name='shark', c_name='attack', c_type='number', value='shark.attack')

    '''activity'''
    c2 = cClass(t_name='shark', c_name='activity', c_type='string', value='shark.activity')

    '''country'''
    c3 = cClass(t_name='shark', c_name='country', c_type='string', value='shark.country')

    '''shark'''
    T = TClass(t_name='shark', c_name=['activity', 'attack', 'country'], c_type=['string', 'number', 'string'])

    l = [c1,c2,c3,T]

    return l

def example_11():
    '''sum of attacks by year and sort in descending order'''

    # '''sum'''
    # f = Sum(None, None, None)
    # f.value = 'lambda(c).F'
    #
    # '''c'''
    # c1 = cClass(t_name='shark', c_name='attack', c_type='number', value='shark.attack')
    #
    # '''by'''
    # G = Group(None, None, None)
    # G.value = 'lambda(F,c).G'
    #
    # '''year'''
    # c2 = cClass(t_name='shark', c_name='year', c_type='string', value='shark.year')

    # '''sort'''
    # s = Order(None,None,None)
    # s.value = 'lambda(c,T,dir).T'
    #
    # '''dir'''
    # dir = Dir(None,None,None,'dec')

    G = Group(None, None, None)
    G.value = 'lambda(F,c).G'

    c1 = cClass(t_name='shark', c_name='attack', c_type='number', value='shark.attack')

    c2 = cClass(t_name='shark', c_name='activity', c_type='string', value='shark.activity')

    l = [G,c2]
    return l

def example_12():
    '''show country, gender and count of sharks in a table''' #测试lambda(T).F T的例子
    c1 = cClass(t_name='shark', c_name='country', c_type='string', value='shark.country')

    c2 = cClass(t_name='shark', c_name='gender', c_type='string', value='shark.gender')

    f = Count(None,None,None)
    f.value = 'lambda(T).F'

    t = TClass(t_name='shark', c_name=['activity', 'attack', 'country', 'gender'], c_type=['string', 'number', 'string','string'])

    l = [c1,c2,f,t]

    return l