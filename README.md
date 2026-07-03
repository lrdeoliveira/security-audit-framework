# Security Audit Framework

Framework de auditoria de segurança (pentest assistido) para aplicações web,
infraestrutura e sistemas com **IA / LLM / MCP**. Orientado a prompts +
automação, organizado em 4 pilares mais um orquestrador.

> Versão **1.3** — metodologia prompt-driven, genérica (use placeholders como
> `{{DESCRICAO_DO_ALVO}}` para adaptar a qualquer produto). Alinhada ao OWASP LLM
> Top 10 **2025**, OWASP ASVS **5.0** e CVSS **4.0** (ver [`CHANGELOG.md`](CHANGELOG.md)).

## Visão geral

| Pilar | Pasta | Objetivo | Fase |
|-------|-------|----------|------|
| **Orquestrador** | `00-orquestrador/` | Planejar escopo, sequência e entregáveis | Pré-auditoria |
| **1. Descobrir** | `01-descobrir/` | Mapear stack, superfície de ataque e componentes de IA | Fase 1 |
| **2. Analisar** | `02-analisar/` | Revisão estática de código, config e IaC (SAST) | Fase 2 |
| **3. Validar** | `03-validar/` | Confirmar explorabilidade (DAST, Red Team, IA) | Fases 3–4 |
| **4. Entregar** | `04-entregar/` | Documentar, priorizar remediação e automatizar reteste | Fase 5 |
| **Templates** | `templates/` | Schema de achados e estrutura de relatório | Transversal |
| **CI/CD** | `ci-cd/` | Pipeline de auditoria contínua (GitHub Actions) | Transversal |

O ponto de entrada completo é [`AUDITORIA.md`](AUDITORIA.md).

## Fluxo

```
bootstrap-scan → plano de ataque → descobrir → analisar → validar → entregar
                                                          ↑__________ reteste __________|
```

1. **Orquestrador** — `00-orquestrador/plano-de-ataque-em-5-fases.md` define o escopo;
   `bootstrap-scan.sh` roda Semgrep, Gitleaks, TruffleHog, Trivy, osv-scanner,
   Checkov e mcp-scan, consolidando o resultado.
2. **Descobrir / Analisar / Validar** — ~35 prompts por categoria (auth, injection,
   path-traversal/SSRF, segredos, cripto, XSS, CORS/CSRF/headers, logging,
   desserialização, IaC, MCP; e para IA, na numeração do **OWASP LLM Top 10 2025**:
   prompt-injection (LLM01), guardrails, RAG e vector/embedding (LLM08), system
   prompt leakage (LLM07), excessive-agency (LLM06), output handling (LLM05),
   denial-of-wallet (LLM10)).
3. **Entregar** — relatório, roadmap de remediação por sprint, mapeamento de
   conformidade (LGPD/GDPR/SOC 2/ISO 27001/ASVS 5.0/PCI DSS/NIST CSF/CIS) e plano
   de reteste por achado.

Cada achado confirmado é registrado em YAML seguindo
[`templates/registro-de-achado.yaml`](templates/registro-de-achado.yaml)
(id, severidade, CVSS 4.0, OWASP, CWE, localização, PoC, impacto, remediação, reteste).

## CI/CD

`ci-cd/security-audit.yml` é um template de GitHub Actions para auditoria
contínua: roda os scanners, quebra o build em achados **CRITICAL** e envia SARIF
para o Code Scanning. Copie para `.github/workflows/` no repositório alvo.

## Uso com agente (Claude Code)

O repositório inclui uma skill que executa o framework de ponta a ponta:
[`.claude/skills/security-audit`](.claude/skills/security-audit/SKILL.md).

Ao abrir este repositório (ou o repositório alvo, com esta skill instalada) no
Claude Code, peça algo como *"faça uma auditoria de segurança deste projeto"* — a
skill confirma a autorização, define o escopo, roda o `bootstrap-scan`, percorre os
pilares na ordem e consolida os achados no schema YAML. Para revisar apenas o diff
atual, use o `/security-review` nativo.

## Uso responsável

Esta metodologia destina-se exclusivamente a **testes de segurança autorizados**:
auditorias de sistemas próprios, engajamentos com autorização formal por escrito,
pesquisa de segurança e fins educacionais. Não a utilize contra sistemas para os
quais você não tenha permissão explícita.

## Licença

[MIT](LICENSE) © 2026 Luciano de Oliveira
