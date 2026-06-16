# Revisão de desserialização e race conditions

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A08:2021 - Software and Data Integrity Failures
**Ferramentas sugeridas:** Semgrep, CodeQL, manual
**Intenção:** Identificar desserialização insegura e condições de corrida (TOCTOU) que permitem RCE, corrupção de estado ou abuso financeiro.

## Como usar
Cole código que desserializa dados não confiáveis (pickle, PHP unserialize, Java/ObjectInputStream, YAML.load, JSON com type hints) e fluxos com operações concorrentes sobre o mesmo recurso (saldo, estoque, cupom, cotas, idempotência).

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO}} | Código de desserialização e/ou fluxos transacionais com concorrência (pagamento, saldo, cotas, estoque) |

## Prompt
```
Atue como especialista em integridade de software e concorrência. Analise {{CODIGO}} e identifique:

DESSERIALIZAÇÃO INSEGURA
(1) Desserialização de dados controláveis pelo usuário com formatos perigosos (pickle, unserialize, ObjectInputStream, yaml.load não-safe, marshal, gadgets conhecidos);
(2) Confiança em dados assinados/serializados sem verificação de integridade (cookies, tokens, cache, filas);
(3) Deploy/atualização sem verificação de integridade (dependências, artefatos, plugins).

RACE CONDITIONS / TOCTOU
(4) Check-then-act sem atomicidade: validar saldo/estoque/cota e depois aplicar em operações separadas;
(5) Falta de lock, transação ou controle de concorrência otimista (versionamento) em recursos compartilhados;
(6) Idempotência ausente em endpoints de pagamento/criação que permitem replay e duplicação;
(7) Double-spend, redeem múltiplo de cupom, bypass de limite por requisições paralelas.

Para cada achado: localização, vetor (payload de desserialização ou sequência de requisições concorrentes) e correção (formato seguro/assinatura; lock, transação atômica, constraint única ou idempotency key).
```

## Saída esperada
Achados de desserialização e de race condition com vetor de exploração e correção (formato seguro, integridade, atomicidade/locking).

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Race conditions identificadas aqui alimentam `03-validar/dast/cenarios-de-abuso-de-logica-de-negocio.md` para confirmação com requisições paralelas. Consulte `AUDITORIA.md` para o checklist completo.
