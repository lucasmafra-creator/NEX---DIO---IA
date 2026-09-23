import os
import streamlit as st
from nex_agent import answer
from data_service import transactions, profile
from financial_engine import total_expenses,total_income,balance,brl

st.set_page_config(page_title='Nex AI — DIO', page_icon='🦉', layout='wide')
st.markdown('''<style>
.block-container{max-width:1100px;padding-top:2rem}.hero{padding:22px;border-radius:22px;background:linear-gradient(135deg,#4b1d7a,#7b3fc7);color:white;margin-bottom:18px}.hero h1{margin:0}.small{opacity:.88}.stChatMessage{border-radius:16px}
</style>''', unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🦉 Nex AI</h1><div class="small">Assistente Financeiro Inteligente • Projeto DIO</div><br><b>A IA explica. O sistema calcula. Os dados comprovam.</b></div>', unsafe_allow_html=True)
rows=transactions(); p=profile()
a,b,c=st.columns(3)
a.metric('Entradas',brl(total_income(rows))); b.metric('Saídas',brl(total_expenses(rows))); c.metric('Saldo calculado',brl(balance(rows)))
st.caption('⚠️ Demonstração educacional com dados 100% fictícios.')
if 'messages' not in st.session_state: st.session_state.messages=[{'role':'assistant','content':'Opa! Sou o Nex 🦉. Quer analisar seus gastos, saldo, metas ou perfil de investimento?'}]
if 'nex_context' not in st.session_state: st.session_state.nex_context={}
for m in st.session_state.messages:
    with st.chat_message(m['role']): st.markdown(m['content'])
if prompt:=st.chat_input('Converse com o Nex...'):
    st.session_state.messages.append({'role':'user','content':prompt})
    with st.chat_message('user'): st.markdown(prompt)
    with st.chat_message('assistant'):
        with st.spinner('Nex está analisando os dados...'):
            resp=answer(prompt,st.session_state.nex_context,True)
        st.markdown(resp)
    st.session_state.messages.append({'role':'assistant','content':resp})
with st.sidebar:
    st.header('🧪 Demonstração')
    st.write('Experimente uma pergunta por vez:')
    st.code('Quanto gastei com alimentação?\nQual categoria teve maior gasto?\nQuanto sobrou?\nComo está minha reserva?\nOnde posso investir?\nQuanto eu gastava há um ano?')
    st.divider(); st.subheader('Base fictícia')
    st.write(f"Cliente: **{p['nome']}**")
    st.write(f"Perfil: **{p['perfil_investidor'].title()}**")
    st.write(f"Objetivo: **{p['objetivo_principal']}**")
    st.divider()
    ai='Ativa' if os.getenv('OPENAI_API_KEY','').strip() else 'Fallback local seguro'
    st.caption(f'Camada generativa: {ai}')
    if st.button('Limpar conversa'):
        st.session_state.messages=[]; st.session_state.nex_context={}; st.rerun()
