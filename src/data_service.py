from pathlib import Path
import csv, json
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
def transactions():
    with open(DATA/'transacoes.csv',encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    for r in rows:r['valor']=float(r['valor'])
    return rows
def profile():
    return json.loads((DATA/'perfil_investidor.json').read_text(encoding='utf-8'))
def products():
    return json.loads((DATA/'produtos_financeiros.json').read_text(encoding='utf-8'))
