import os
from data_service import transactions, profile, products
from financial_engine import total_category, totals_by_category, total_expenses, total_income, balance, brl, norm

SYSTEM_PROMPT = """Você é Nex, um assistente financeiro educativo. Responda em português do Brasil, de forma clara, amigável e não julgadora. Use SOMENTE os fatos financeiros fornecidos no CONTEXTO VALIDADO. Nunca invente valores, datas, saldos ou transações. Se algo não estiver no contexto, diga que não há dados suficientes. Diferencie fatos de sugestões. Não prometa retorno de investimento e nunca peça senhas, PINs ou tokens. Seja conciso."""

def detect_category(text):
    t=norm(text)
    aliases={'alimentacao':['alimentacao','comida','mercado','restaurante'],'moradia':['moradia','casa','aluguel'],'transporte':['transporte','uber','combustivel'],'saude':['saude','farmacia','academia'],'lazer':['lazer','netflix']}
    for c,words in aliases.items():
        if any(w in t for w in words): return c
    return None

def build_facts(message, state=None):
    state=state if state is not None else {}
    rows=transactions(); p=profile(); t=norm(message); cat=detect_category(message)
    if cat: state['last_category']=cat
    if any(x in t for x in ['senha','pin','token','codigo de autenticacao']): return {'kind':'security','text':'Credenciais bancárias não estão disponíveis e não devem ser solicitadas.'}
    if 'previsao do tempo' in t or 'clima' in t: return {'kind':'out','text':'Pergunta fora do escopo financeiro do protótipo.'}
    if ('ano' in t and any(x in t for x in ['gaste','gasto','gastava'])) or '6 meses' in t or 'seis meses' in t: return {'kind':'missing','text':'A base contém somente transações de outubro de 2025; não há dados do período solicitado.'}
    if ('quanto' in t or 'gaste' in t or 'gasto' in t) and (cat or state.get('last_category')):
        c=cat or state['last_category']; v=total_category(rows,c)
        return {'kind':'fact','text':f'Categoria: {c}. Total calculado: {brl(v)}. Período disponível: outubro de 2025.'}
    if 'categoria' in t and any(x in t for x in ['maior','mais gasto','mais gaste']):
        d=totals_by_category(rows); c,v=max(d.items(),key=lambda x:x[1]); return {'kind':'fact','text':f'Maior categoria de saída: {c}. Total: {brl(v)}.'}
    if any(x in t for x in ['saldo','sobrou','disponivel','entrou','saiu','receita','despesa']):
        return {'kind':'fact','text':f'Entradas: {brl(total_income(rows))}. Saídas: {brl(total_expenses(rows))}. Saldo calculado: {brl(balance(rows))}.'}
    if 'reserva' in t or 'meta' in t:
        meta=p['metas'][0]['valor_necessario']; atual=p['reserva_emergencia_atual']; falta=max(meta-atual,0); prog=(atual/meta*100 if meta else 0)
        return {'kind':'fact','text':f'Reserva atual: {brl(atual)}. Meta: {brl(meta)}. Falta: {brl(falta)}. Progresso: {prog:.1f}%.'}
    if 'invest' in t:
        opts=[x for x in products() if x['risco'] in ('baixo','medio')]
        desc='; '.join(f"{x['nome']} (risco {x['risco']}, {x['rentabilidade']})" for x in opts[:4])
        return {'kind':'fact','text':f"Perfil cadastrado: {p['perfil_investidor']}. Objetivo: {p['objetivo_principal']}. Produtos fictícios disponíveis para explicação: {desc}. Não há garantia de retorno."}
    if any(x in t for x in ['oi','ola','olá','opa','bom dia','boa tarde','boa noite']): return {'kind':'greeting','text':'O usuário iniciou uma conversa.'}
    return {'kind':'missing','text':'Não há fatos suficientes na base para responder à pergunta com segurança.'}

def deterministic_reply(facts):
    k=facts['kind']; x=facts['text']
    if k=='security': return 'Não tenho acesso a senhas, PINs ou códigos de autenticação e não posso fornecer credenciais.'
    if k=='out': return 'Essa não é muito minha área 😅. Meu foco aqui é ajudar com organização financeira.'
    if k=='missing': return 'Não tenho dados suficientes para responder isso com segurança. ' + x
    if k=='greeting': return 'Opa! Sou o Nex 🦉. Posso analisar gastos, saldo, categorias, metas e informações de investimento usando a base fictícia do projeto.'
    return x

def llm_reply(message, facts):
    key=os.getenv('OPENAI_API_KEY','').strip()
    if not key: return None
    try:
        from openai import OpenAI
        client=OpenAI(api_key=key)
        model=os.getenv('OPENAI_MODEL','gpt-5.6-luna')
        r=client.responses.create(model=model, instructions=SYSTEM_PROMPT, input=f'CONTEXTO VALIDADO:\n{facts["text"]}\n\nUSUÁRIO:\n{message}')
        return (r.output_text or '').strip() or None
    except Exception:
        return None

def answer(message, state=None, use_ai=True):
    facts=build_facts(message,state)
    if facts['kind'] in ('security','out','missing','greeting'): return deterministic_reply(facts)
    if use_ai:
        generated=llm_reply(message,facts)
        if generated: return generated
    return deterministic_reply(facts)
