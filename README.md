# 🦉 Nex AI — Assistente Financeiro Inteligente

Projeto final do Lab **Construa Seu Assistente Virtual Com Inteligência Artificial**, da DIO.

O Nex é um protótipo de assistente financeiro que conversa sobre uma base fictícia, executa cálculos financeiros em código e pode usar IA generativa para transformar fatos validados em respostas naturais.

> **A IA explica. O sistema calcula. Os dados comprovam.**

## 🎯 Objetivo
Ajudar uma pessoa a compreender gastos, saldo, categorias, metas e informações financeiras sem inventar dados quando a informação não estiver disponível.

## ✨ Funcionalidades
- Chat interativo em Streamlit
- Gastos por categoria
- Maior categoria de despesas
- Entradas, saídas e saldo
- Acompanhamento de reserva/meta
- Perfil e produtos financeiros fictícios
- Continuidade simples de contexto
- Tratamento de dados ausentes
- Proteção contra pedidos de credenciais
- Camada generativa opcional via OpenAI API
- Fallback local determinístico quando não há API
- Testes automatizados

## 🧠 Arquitetura
`Usuário → intenção/contexto → dados CSV/JSON → cálculos determinísticos → contexto validado → IA (opcional) → resposta`

Valores críticos são calculados pelo código antes de chegarem ao modelo. A IA não é usada como fonte dos números.

## 📁 Estrutura
```text
Nex_AI_DIO/
├── README.md
├── requirements.txt
├── .env.example
├── data/
├── docs/
├── src/
└── tests/
```

## 🚀 Executar no Windows
```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run src/app.py
```

O projeto funciona sem chave de API usando o fallback local seguro.

### Ativar IA generativa (opcional)
Defina a variável `OPENAI_API_KEY` no seu ambiente. Nunca coloque a chave real no GitHub. O modelo pode ser configurado por `OPENAI_MODEL`.

## 🧪 Testes
```bat
pytest -q
```

Os testes cobrem cálculos, contexto, dados ausentes, segurança, escopo, reserva e investimento.

## 💬 Perguntas para demonstração
- Quanto gastei com alimentação?
- Qual categoria teve maior gasto?
- Quanto sobrou?
- Como está minha reserva?
- Onde posso investir?
- Quanto eu gastava com alimentação há um ano?
- Qual minha senha bancária?

## 🗃️ Dados
Todos os dados presentes em `data/` são fictícios e utilizados exclusivamente para fins educacionais.

## 🛡️ Segurança e anti-alucinação
O Nex não deve inventar valores, preencher períodos ausentes como se fossem reais, solicitar credenciais ou apresentar retorno de investimento como garantia. Quando faltam dados, ele declara a limitação.

## 📚 Documentação
Os arquivos em `docs/` registram documentação do agente, base de conhecimento, prompts, métricas e roteiro do pitch.

## 👨‍💻 Autor
**Lucas Mafra** — projeto educacional e de portfólio desenvolvido para a DIO.
