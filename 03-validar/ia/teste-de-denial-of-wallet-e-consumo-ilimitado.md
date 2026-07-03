# Teste de denial-of-wallet e consumo ilimitado

**Pilar:** validar
**Fase:** 4
**Categoria:** ia
**OWASP:** LLM10:2025 - Unbounded Consumption
**Ferramentas sugeridas:** Manual, scripts próprios, Promptfoo
**Intenção:** Verificar se o sistema de IA tem limites de custo, tokens e recursos — protegendo contra denial-of-wallet, DoS de modelo e extração.

## Como usar
Descreva como o produto cobra/consome IA: modelos usados, custo por token, cotas por plano, limites de contexto, se há cache, e quais ações disparam chamadas de LLM (incluindo loops de agente e tools encadeadas).

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{DESCRICAO_DO_CONSUMO}} | Modelos, custo por token, cotas por plano/usuário, limites de contexto e gatilhos de chamadas de IA |

## Prompt
```
Atue como especialista em abuso de custo e disponibilidade de sistemas de IA (LLM10). Para {{DESCRICAO_DO_CONSUMO}}, elabore testes para:

(1) Denial-of-wallet: maximizar custo por requisição (input grande, max_tokens alto, forçar saída longa) e por volume (sem rate-limit/cota por usuário);
(2) Amplificação por agente: prompts que disparam muitos passos, tools encadeadas, recursão ou loops de raciocínio sem teto;
(3) Exaustão de contexto: estourar a janela de contexto para degradar serviço ou elevar custo a cada turno;
(4) Bypass de cota: múltiplas contas/tenants, troca de chave, race no contador, endpoints alternativos sem limite;
(5) DoS de modelo: entradas que causam latência alta, payloads que travam tokenização/parsing, uploads grandes para pipelines multimodais/RAG;
(6) Extração de modelo/sistema: consultas em massa para destilar comportamento ou reconstruir o system prompt/base de conhecimento;
(7) Custo via fan-out (cruza com LLM08:2025 - Vector and Embedding Weaknesses): uma ação do usuário que gera N embeddings/buscas/gerações sem limite — o pipeline de embeddings/RAG é superfície de custo.

Para cada teste: ação, como medir tokens/custo/latência, sinais de ausência de limite e estimativa de impacto financeiro. Use volumes pequenos para provar a ausência de teto — não gere custo real significativo.
```

## Saída esperada
Plano de teste de consumo com método de medição de custo/tokens/latência, técnicas de bypass de cota e estimativa de impacto financeiro.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 4 - Red teaming de IA. Faça par com `03-validar/dast/teste-de-rate-limiting-brute-force-e-dos.md`. Crítico para SaaS com IA: o impacto é financeiro direto. Combine volumes com o dono do ambiente. Consulte `AUDITORIA.md` para o checklist completo.
