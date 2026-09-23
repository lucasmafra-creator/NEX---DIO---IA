import unicodedata
from collections import defaultdict
def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
def brl(v):
    return f'R$ {v:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
def expenses(rows): return [r for r in rows if r['tipo']=='saida']
def total_category(rows, category):
    c=norm(category)
    return sum(r['valor'] for r in expenses(rows) if norm(r['categoria'])==c)
def totals_by_category(rows):
    d=defaultdict(float)
    for r in expenses(rows): d[r['categoria']]+=r['valor']
    return dict(d)
def total_expenses(rows): return sum(r['valor'] for r in expenses(rows))
def total_income(rows): return sum(r['valor'] for r in rows if r['tipo']=='entrada')
def balance(rows): return total_income(rows)-total_expenses(rows)
