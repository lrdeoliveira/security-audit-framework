# Bootstrap de scan automatizado

**Pilar:** orquestrador
**Fase:** 1–2 (ingestão)
**Categoria:** automação
**OWASP:** —
**Ferramentas sugeridas:** Semgrep, Gitleaks, TruffleHog, Trivy, osv-scanner, Checkov, mcp-scan, jq
**Intenção:** Rodar os scanners base de uma vez e consolidar a saída em `pre-scan.md`, eliminando a cópia manual de código nos prompts do Pilar 2 e garantindo que nenhuma classe automatizável seja esquecida.

## Por que existe
O framework é prompt-driven: sem automação, o auditor cola código manualmente em cada prompt. O bootstrap inverte isso — os scanners varrem o repo primeiro e produzem um resumo priorizado que alimenta os prompts. Ganho típico: horas por auditoria e cobertura consistente do baseline (SAST, segredos, SCA, IaC, MCP).

## Como usar

```bash
# 1. Tornar executável (uma vez)
chmod +x 00-orquestrador/bootstrap-scan.sh

# 2. Rodar contra o repo alvo
./00-orquestrador/bootstrap-scan.sh /caminho/do/repo <produto> [YYYY-MM-DD]

# Exemplo
./00-orquestrador/bootstrap-scan.sh ~/projetos/minha-app minha-app
```

Saída:

```
auditorias/<produto>-<data>/
├── pre-scan.md          # resumo consolidado e priorizado (entrada do Pilar 2)
├── raw-scans/           # saídas brutas de cada scanner (json/txt)
└── evidencias/          # criado vazio, pronto para o Pilar 3
```

O script executa apenas os scanners instalados e pula os demais com aviso — não falha se faltar ferramenta.

## Instalação dos scanners

```bash
# macOS (Homebrew)
brew install semgrep gitleaks trufflehog trivy osv-scanner checkov jq
pipx install mcp-scan        # ou: pip install mcp-scan

# Linux
pipx install semgrep checkov mcp-scan
# trivy:       https://trivy.dev/latest/getting-started/installation/
# gitleaks:    go install github.com/gitleaks/gitleaks/v8@latest  (ou release no GitHub)
# trufflehog:  curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
# osv-scanner: go install github.com/google/osv-scanner/v2/cmd/osv-scanner@latest
```

## O que cada scanner cobre

| Scanner | Cobertura | Prompt que alimenta (com o pilar no caminho) |
|---------|-----------|----------------------------------------------|
| Semgrep | SAST (injection, auth, XSS, etc.) | todos os de `02-analisar/` |
| Gitleaks | segredos no histórico git | `02-analisar/analise-de-segredos-e-configuracao-insegura.md` |
| TruffleHog | segredos **verificados** (ativos) | idem — prioridade máxima |
| Trivy | SCA + IaC + secrets | `01-descobrir/analise-de-package-manifest-e-dependencias.md`, `02-analisar/revisao-de-iac-gerado-por-ia.md` |
| osv-scanner | SCA (fallback OSV) | `01-descobrir/analise-de-package-manifest-e-dependencias.md` |
| Checkov | IaC misconfig | `02-analisar/revisao-de-iac-gerado-por-ia.md` |
| mcp-scan | escopo/over-permission de MCP | `02-analisar/analise-de-configuracao-de-mcp-e-escopo-de-tools.md` |

## Saída esperada
`pre-scan.md` com contagens, top findings por categoria, inventário de stack e checklist de próximos passos manuais.

## Onde usar no fluxo
Início da Fase 1/2. Rode logo após definir o escopo e antes de abrir os prompts do Pilar 2. Triague o resultado: descarte falsos positivos, promova o resto a `rascunho` em `achados.yaml`. Consulte `AUDITORIA.md` para o checklist completo.
