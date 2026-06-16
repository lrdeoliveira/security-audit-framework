# Análise de configuração de MCP e escopo de tools

**Pilar:** analisar
**Fase:** 2 / 4
**Categoria:** agent
**OWASP:** LLM06 - Excessive Agency
**Ferramentas sugeridas:** mcp-scan, Manual
**Intenção:** Revisar configuração de servidor MCP para identificar over-permission e riscos de agente.

## Como usar
Cole o arquivo de configuração do servidor MCP ou a definição das tools. Inclua o contexto de uso: que tipo de agente usa este MCP e quais tarefas executa.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{DESCRICAO_DO_AGENTE}} | Tipo de agente, suas tarefas declaradas e nível de confianca esperado |
| {{CONFIGURACAO_MCP}} | Arquivo de configuração do servidor MCP ou lista de tools com nome, descrição e parâmetros |

## Prompt
```
Atue como especialista em segurança de sistemas MCP. Analise a configuração de servidor MCP do agente {{DESCRICAO_DO_AGENTE}} utilizando a configuração: {{CONFIGURACAO_MCP}}. Avalie:

(1) Escopo de cada tool versus necessidade declarada: alguma tool tem acesso mais amplo do que o caso de uso justifica?
(2) Parametros sem validação em tools que executam ações de alto impacto;
(3) Tools com side effects irreversiveis sem mecanismo de confirmação ou rollback;
(4) Descricoes de tools vagas ou enganosas que poderiam levar o modelo a chamar a tool em contexto errado;
(5) Ausencia de logging ou auditoria de tool calls;
(6) Superficie de tool poisoning: se o servidor MCP for comprometido, qual e o impacto máximo?
```

## Saída esperada
Auditoria de configuração MCP com over-permission identificado, riscos e configuração de escopo mínimo recomendada.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática / Fase 4 - Red teaming de IA. Use em conjunto com mcp-scan. Consulte `AUDITORIA.md` para o checklist completo.
