# Documentação do Agente

## Caso de uso
O Nex ajuda usuários a transformar dados financeiros em informações fáceis de compreender. O protótipo atende pessoas que desejam analisar gastos, saldo, categorias, metas e informações de investimento.

## Persona
**Nome:** Nex  
**Personalidade:** amigável, consultiva, educativa e não julgadora.  
**Tom:** acessível, direto e natural.

## Arquitetura simplificada
```mermaid
flowchart TD
A[Usuário] --> B[Interface Streamlit]
B --> C[Motor do Nex]
C --> D[Base CSV/JSON]
D --> E[Cálculos determinísticos]
E --> F[Contexto validado]
F --> G[IA Generativa opcional]
G --> H[Resposta]
F --> I[Fallback local seguro]
I --> H
```

## Segurança
- Não inventar valores financeiros.
- Declarar ausência de dados.
- Não solicitar ou revelar credenciais.
- Diferenciar informação de sugestão.
- Não garantir retorno de investimentos.
- Preservar a decisão final do usuário.
