# Security Audit Framework

Framework de auditoria de segurança (pentest assistido) para aplicações web,
infraestrutura e sistemas com **IA / LLM / MCP**. Orientado a prompts +
automação de alto rendimento, organizado em 4 pilares mais um orquestrador.

> Versão **1.4** — metodologia prompt-driven com automação CLI, ingestão concorrente,
> validação de schema e geração de laudos. Alinhada ao OWASP LLM Top 10 **2025**,
> OWASP ASVS **5.0** e CVSS **4.0** (ver [`CHANGELOG.md`](CHANGELOG.md)).

## Visão geral

| Pilar | Pasta | Objetivo | Fase |
|---|---|---|---|
| **Orquestrador** | `00-orquestrador/` | Planejar escopo, ingestão paralela e entregáveis | Pré-auditoria |
| **1. Descobrir** | `01-descobrir/` | Mapear stack, superfície de ataque e componentes de IA | Fase 1 |
| **2. Analisar** | `02-analisar/` | Revisão estática de código, config e IaC (SAST) | Fase 2 |
| **3. Validar** | `03-validar/` | Confirmar explorabilidade (DAST, Red Team, IA) | Fases 3–4 |
| **4. Entregar** | `04-entregar/` | Documentar, priorizar remediação e automatizar reteste | Fase 5 |
| **Automação** | `scripts/` | CLI `audit_tool.py` (ingestão, validação, laudos, select) | Transversal |
| **Catálogo** | `catalog/` | Índice estruturado de prompts para economia de tokens de IA | Transversal |
| **Templates** | `templates/` | Schema de achados YAML e estrutura de relatório | Transversal |
| **CI/CD** | `ci-cd/` | Pipeline de auditoria contínua (GitHub Actions com cache) | Transversal |

O ponto de entrada completo é [`AUDITORIA.md`](AUDITORIA.md).

## Fluxo Automatizado v1.4

```
make scan (paralelo) ──> make ingest (achados.yaml) ──> DAST/IA ──> make validate ──> make report
                                                             ↑______ reteste _______|
```

1. **Varredura Base (Concorrente):**
   ```bash
   make scan REPO=/caminho/do/alvo PROD=minha-app
   # Executa Semgrep, Gitleaks, TruffleHog, Trivy, OSV e Checkov em paralelo (3x-5x mais rápido).
   ```
2. **Ingestão Automática de Achados:**
   ```bash
   make ingest AUDIT=auditorias/minha-app-YYYY-MM-DD
   # Converte saídas brutas (JSON) diretamente em rascunhos estruturados em achados.yaml com CWE e OWASP.
   ```
3. **Seleção de Prompts Otimizada (Economia de Tokens):**
   ```bash
   make select STACK=laravel,vue,ia,docker
   # Retorna apenas os prompts relevantes ao stack, evitando carregar 40 arquivos de prompt no LLM.
   ```
4. **Validação de Qualidade e Integridade:**
   ```bash
   make validate AUDIT=auditorias/minha-app-YYYY-MM-DD
   # Garante conformidade de enums, CVSS 4.0, integridade de deriva_de e consistência das estatísticas.
   ```
5. **Geração do Laudo Final:**
   ```bash
   make report AUDIT=auditorias/minha-app-YYYY-MM-DD
   # Compila automaticamente achados.yaml no relatório executivo e técnico relatorio-final.md.
   ```

## CI/CD

`ci-cd/security-audit.yml` é um template de GitHub Actions para auditoria
contínua: roda os scanners com cache de banco de vulnerabilidades (Trivy),
quebra o build em achados **CRITICAL** e envia SARIF para o Code Scanning.
Copie para `.github/workflows/` no repositório alvo.

## Uso com Agentes de IA

O framework suporta nativamente agentes autônomos (**Antigravity**, **Claude Code**, **Cursor**, **Codex**):
- Instruções detalhadas para agentes: [`AGENTS.md`](AGENTS.md)
- Skill Claude: [`.claude/skills/security-audit/SKILL.md`](.claude/skills/security-audit/SKILL.md)
- Skill Antigravity/Redfox: [`skills/security-audit/SKILL.md`](skills/security-audit/SKILL.md)
- Regra Cursor: [`.cursor/rules/auditoria-seguranca.mdc`](.cursor/rules/auditoria-seguranca.mdc)

## Uso responsável

Esta metodologia destina-se exclusivamente a **testes de segurança autorizados**:
auditorias de sistemas próprios, engajamentos com autorização formal por escrito,
pesquisa de segurança e fins educacionais. Não a utilize contra sistemas para os
quais você não tenha permissão explícita.

## Licença

[MIT](LICENSE) © 2026 Luciano de Oliveira
