
def get_table():
    #t_name = 'shark_attack'
    #Table = {"country":'string', 'gender':'string', 'fatality':'string','activity':'string','attack':'number','year':'date', 'count(t)':'number'}
    t_name = 'job'
    Table = {'field': 'string', 'title': 'string', 'posting_date': 'date', 'desired_year_experience': 'number',
             'required_academic_qualification': 'string', 'company': 'string', 'area': 'string',
             'city': 'string', 'country': 'string', 'programming_language': 'string', 'salary': 'number',
             'plantform': 'string', 'count(t)': 'number'
             }
    return t_name, Table