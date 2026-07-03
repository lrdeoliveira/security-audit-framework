# Análise de configuração de MCP e escopo de tools

**Pilar:** analisar
**Fase:** 2 / 4
**Categoria:** sast
**OWASP:** LLM06:2025 - Excessive Agency (+ LLM01:2025 Prompt Injection, LLM03:2025 Supply Chain)
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

(1) Escopo de cada tool versus necessidade declarada: alguma tool tem acesso mais amplo do que o caso de uso justifica? Avalie também o escopo das credenciais do próprio servidor MCP (token/OAuth), não só das tools;
(2) Parâmetros sem validação em tools que executam ações de alto impacto; command injection/SSRF na implementação da própria tool;
(3) Tools com side effects irreversíveis sem mecanismo de confirmação ou rollback; human-in-the-loop ausente para ações destrutivas;
(4) Tool poisoning: instruções maliciosas embutidas na `description` ou em nomes de parâmetro que o modelo lê e obedece;
(5) Confused deputy: o servidor usa credenciais amplas em nome de input não confiável;
(6) Rug pull / TOCTOU de definição de tool: a definição muda depois de aprovada pelo usuário;
(7) Cross-server tool shadowing: servidor malicioso sobrescreve tool de servidor confiável;
(8) Token/credential passthrough: MCP guardando ou repassando OAuth de escopo amplo;
(9) Ausência de logging ou auditoria de tool calls;
(10) Superfície de comprometimento: se o servidor MCP for comprometido, qual é o impacto máximo?
```

## Saída esperada
Auditoria de configuração MCP com over-permission identificado, riscos e configuração de escopo mínimo recomendada.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática / Fase 4 - Red teaming de IA. Use em conjunto com mcp-scan. Consulte `AUDITORIA.md` para o checklist completo.
