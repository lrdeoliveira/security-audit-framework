# Identificação de componentes de IA e vetores específicos

**Pilar:** descobrir
**Fase:** 1
**Categoria:** recon
**OWASP:** LLM01 - Prompt Injection
**Ferramentas sugeridas:** Manual
**Intenção:** Mapear onde LLMs, agentes e MCPs estao integrados e quais vetores de ataque se aplicam.

## Como usar
Cole o código que interage com LLMs, a definição de tools/functions, o system prompt (se acessivel) e qualquer configuração de agente.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_DE_IA}} | Código de integração com LLM, definição de tools, system prompt ou configuração de agente |

## Prompt
```
Análise {{CODIGO_DE_IA}} e produza um mapa de componentes de IA com:

(1) LLMs ou APIs de modelo usados e sua configuração: temperatura, max tokens, system prompt;
(2) System prompts identificados ou inferidos;
(3) Tools e functions disponíveis para o modelo com seus parâmetros;
(4) Fontes de dados injetadas no contexto: RAG, banco, memória;
(5) Fluxo de dados do usuário ate o modelo e do modelo ate a execução;
(6) Vetores de ataque específicos: prompt injection, excessive agency, tool poisoning, exfiltração.

Classifique cada vetor por probabilidade e impacto.
```

## Saída esperada
Mapa de componentes com vetores de ataque priorizados e recomendações de teste.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 1 - Reconhecimento. Execute antes do red teaming de IA para orientar a estrategia de ataque. Consulte `AUDITORIA.md` para o checklist completo.
