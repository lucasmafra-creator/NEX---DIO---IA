import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from data_service import transactions
from financial_engine import total_category,total_expenses,total_income,balance,totals_by_category
from nex_agent import answer,build_facts

def test_calculos_exatos():
    r=transactions(); assert total_category(r,'alimentacao')==570.0; assert total_income(r)==5000.0; assert total_expenses(r)==2488.9; assert round(balance(r),2)==2511.1

def test_maior_categoria(): assert max(totals_by_category(transactions()),key=totals_by_category(transactions()).get)=='moradia'
def test_resposta_categoria(): assert 'R$ 570,00' in answer('Quanto gastei com alimentação?',{},False)
def test_maior_categoria_resposta(): assert 'moradia' in answer('Qual categoria teve maior gasto?',{},False).lower()
def test_ausencia_periodo(): assert 'não tenho dados suficientes' in answer('Quanto eu gastava com alimentação há um ano?',{},False).lower()
def test_seguranca(): assert 'não tenho acesso' in answer('Qual minha senha bancária?',{},False).lower()
def test_fora_escopo(): assert 'não é muito minha área' in answer('Qual a previsão do tempo?',{},False).lower()
def test_contexto():
    s={}; answer('Quanto gastei com alimentação?',s,False); assert '570,00' in answer('E quanto gastei?',s,False)
def test_reserva():
    x=answer('Como está minha reserva?',{},False); assert '10.000,00' in x and '15.000,00' in x and '5.000,00' in x
def test_investimento_sem_garantia(): assert 'Não há garantia de retorno' in build_facts('Onde posso investir?',{})['text']
