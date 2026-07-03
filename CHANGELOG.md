# Changelog

Todas as mudanças relevantes do Security Audit Framework. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [1.3] — 2026-07-03

### Corrigido (bugs / prompts quebrados)
- **CI:** dois SHAs de actions eram inválidos (alucinados) e quebravam o pipeline na
  primeira execução — `actions/checkout@v5.0.0` e `gitleaks/gitleaks-action@v3.0.0`
  agora usam o SHA de commit real (validado via API do GitHub).
- **`02-analisar/analise-de-criptografia`:** o prompt tinha um nome de produto real
  hardcoded no lugar do placeholder `{{CODIGO_DE_CRIPTO}}` — corrigido (era prompt
  quebrado + vazamento de marca em repo público).
- **`03-validar/ia/analise-de-tool-use-e-excessive-agency`:** prompt quebrado (texto
  de teste vazado) sem usar `{{NOME_DO_AGENTE}}`/`{{LISTA_DE_TOOLS}}` — corrigido.
- **`03-validar/dast/analise-de-resposta-e-vazamento-de-informacao`:** nome de produto
  real vazado no prompt e placeholder `{{RESPOSTAS_HTTP}}` não usado — corrigido.
- **`bootstrap-scan.sh`:** contagem do TruffleHog imprimia "0 0" quando não havia
  match (`grep -c || echo 0`); `gitleaks detect` (deprecado) → `gitleaks git`;
  `mcp-scan` agora recebe os arquivos de config (antes recebia o diretório do repo).

### Currency (padrões atualizados)
- **OWASP LLM Top 10 2025** aplicado a todos os prompts de IA, incluindo as duas
  categorias novas de 2025: **LLM07 System Prompt Leakage** e **LLM08 Vector and
  Embedding Weaknesses**. Reetiquetados: RAG (`LLM03`→`LLM08:2025`), system-prompt
  (`LLM01`→`LLM07:2025`), guardrails (`LLM06`→`LLM01:2025`).
- **OWASP ASVS 5.0** (notação `v5.0.0-x.y.z`) no mapeamento de conformidade.
- **CVSS 4.0** como padrão no schema, ficha técnica e relatório (3.1 aceito p/ legado).
- **OWASP Top 10 2025** (A03 Software Supply Chain) citado no prompt de dependências.

### Adicionado (cobertura)
- **IA:** memory poisoning persistente, taxonomia de jailbreak (many-shot, crescendo,
  skeleton key, ASCII/Unicode smuggling), fraquezas de embedding, PyRIT como ferramenta.
- **MCP:** tool poisoning, confused deputy, rug pull, cross-server shadowing, token
  passthrough, human-in-the-loop para ações destrutivas.
- **Web:** SSRF a metadados de cloud (169.254.169.254), single-packet attack para race
  conditions, JWT alg confusion/`jku`, XXE em OOXML, sinks perigosos por linguagem
  (Go/PHP/Node/Python), bind `127.0.0.1` e hardening de K8s no prompt de IaC.
- **Descobrir:** protocolos modernos (GraphQL/WebSockets/SSE/gRPC), source maps,
  proveniência de modelos, dependency confusion; padrões de grep concretos.
- **Entrega:** relatório com disclaimer legal, metodologia, matriz de risco, seção de
  conformidade, resultados de reteste e histórico do documento; SLA por severidade e
  aceite formal de risco no roadmap; NIST CSF 2.0 e CIS Controls v8.1 na conformidade.

### CI/CD
- Permissões *least privilege* por job; imagem do Semgrep fixada por digest; gate de
  SAST (falha em regras `ERROR`); gate de IaC/misconfig no Trivy; `dependency-review`
  em PR; `GITLEAKS_LICENSE` documentado para repos de organização; `semgrep --metrics=off`.

### Consistência
- Correção de gramática/acentuação PT-BR nos prompts do lote antigo ("Análise"→"Analise",
  "Você e"→"Você é"); `Categoria: agent`→`ia` e `red-team`→`dast` onde divergia do schema;
  `.cursor/rules` sem caminho externo ao repo; `.gitignore` reforçado (segredos + `auditorias/**`).

## [1.2] — 2026-06-16
- Generalização com placeholders (`{{DESCRICAO_DO_ALVO}}` etc.); actions do CI fixadas
  por versão/SHA; schema do `achados.yaml` documentado no `AUDITORIA.md`.

## [1.1] — 2026-06-16
- Pilares de conteúdo (XSS/CORS/logging/desserialização; DAST auth/rate-limit/DoS;
  IA LLM05/LLM10; conformidade). Renomeação de 23 arquivos com mojibake.

## [1.0]
- Release inicial: 5 fases, 4 pilares, bootstrap-scan e templates.
