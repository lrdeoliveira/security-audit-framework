#!/usr/bin/env bash
# ============================================================================
# bootstrap-scan.sh — Ingestão automatizada do Pilar 1/2 (Descobrir + Analisar)
# Framework de Auditoria de Segurança v1.3
#
# Roda os scanners base sobre um repositório e consolida a saída em um único
# pre-scan.md, que alimenta os prompts do Pilar 2 (Analisar) sem cópia manual.
#
# Uso:
#   ./00-orquestrador/bootstrap-scan.sh <caminho_do_repo> <produto> [data]
#
# Exemplo:
#   ./00-orquestrador/bootstrap-scan.sh ~/projetos/minha-app minha-app
#
# Saída:
#   auditorias/<produto>-<data>/pre-scan.md          (resumo consolidado)
#   auditorias/<produto>-<data>/raw-scans/*.json|txt (saídas brutas)
#
# Scanners (executa os que estiverem instalados; pula o resto com aviso):
#   semgrep      - SAST (regras auto + segurança)
#   gitleaks     - segredos no histórico git
#   trufflehog   - segredos verificados (filesystem)
#   trivy        - SCA / vulnerabilidades em dependências + IaC + secrets
#   osv-scanner  - vulnerabilidades em dependências (OSV)
#   checkov      - IaC misconfig (Terraform/CloudFormation/K8s/Docker)
#   mcp-scan     - escopo/risco de servidores MCP (se houver config MCP)
# ============================================================================

set -uo pipefail

# ---------- args ----------
REPO="${1:-}"
PRODUTO="${2:-}"
DATA="${3:-$(date +%Y-%m-%d)}"

if [[ -z "$REPO" || -z "$PRODUTO" ]]; then
  echo "Uso: $0 <caminho_do_repo> <produto> [data YYYY-MM-DD]" >&2
  exit 1
fi
if [[ ! -d "$REPO" ]]; then
  echo "ERRO: repositório não encontrado: $REPO" >&2
  exit 1
fi

# diretório do framework (raiz = pai de 00-orquestrador)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTDIR="$ROOT/auditorias/${PRODUTO}-${DATA}"
RAW="$OUTDIR/raw-scans"
PRESCAN="$OUTDIR/pre-scan.md"
mkdir -p "$RAW" "$OUTDIR/evidencias"

ts() { date "+%Y-%m-%d %H:%M:%S"; }
have() { command -v "$1" >/dev/null 2>&1; }
log() { echo "[$(ts)] $*"; }

# cabeçalho do pre-scan
{
  echo "# Pre-scan automatizado — ${PRODUTO}"
  echo
  echo "- **Repo:** \`$REPO\`"
  echo "- **Data:** $DATA"
  echo "- **Gerado por:** bootstrap-scan.sh (Framework v1.3)"
  echo
  echo "> Saídas brutas em \`raw-scans/\`. Use este resumo como entrada dos prompts do Pilar 2."
  echo
} > "$PRESCAN"

section() { echo -e "\n---\n\n## $1\n" >> "$PRESCAN"; }
skip()    { log "SKIP $1 (não instalado)"; echo "_Scanner \`$1\` não instalado — pulado._" >> "$PRESCAN"; }

# ---------- 1. Semgrep (SAST) ----------
section "SAST — Semgrep"
if have semgrep; then
  log "Rodando semgrep..."
  # --metrics=off: não enviar telemetria/metadados (auditoria de código confidencial)
  semgrep scan --config auto --metrics=off --severity ERROR --severity WARNING \
    --json --output "$RAW/semgrep.json" "$REPO" >/dev/null 2>&1
  if have jq && [[ -f "$RAW/semgrep.json" ]]; then
    total=$(jq '.results | length' "$RAW/semgrep.json" 2>/dev/null || echo "?")
    echo "**Total de findings:** $total" >> "$PRESCAN"
    echo >> "$PRESCAN"
    echo "Top regras por frequência:" >> "$PRESCAN"; echo >> "$PRESCAN"
    jq -r '.results[].check_id' "$RAW/semgrep.json" 2>/dev/null \
      | sort | uniq -c | sort -rn | head -20 \
      | awk '{c=$1; $1=""; printf "- `%s` — %s ocorrência(s)\n", substr($0,2), c}' >> "$PRESCAN"
  else
    echo "Saída em \`raw-scans/semgrep.json\` (instale \`jq\` para resumo)." >> "$PRESCAN"
  fi
else
  skip semgrep
fi

# ---------- 2. Gitleaks (segredos no git) ----------
section "Segredos — Gitleaks (histórico git)"
if have gitleaks; then
  if [[ -d "$REPO/.git" ]]; then
    log "Rodando gitleaks..."
    # `gitleaks git <path>` varre o histórico (o antigo `detect --source` está deprecado desde a v8.19)
    gitleaks git "$REPO" --report-format json \
      --report-path "$RAW/gitleaks.json" --redact >/dev/null 2>&1
    if have jq && [[ -f "$RAW/gitleaks.json" ]]; then
      n=$(jq 'length' "$RAW/gitleaks.json" 2>/dev/null || echo "?")
      echo "**Segredos potenciais (redacted):** $n" >> "$PRESCAN"; echo >> "$PRESCAN"
      jq -r '.[] | "- \(.RuleID) em `\(.File)` (commit \(.Commit[0:8]))"' \
        "$RAW/gitleaks.json" 2>/dev/null | head -30 >> "$PRESCAN"
    fi
  else
    echo "_Sem diretório .git — gitleaks pulado._" >> "$PRESCAN"
  fi
else
  skip gitleaks
fi

# ---------- 3. TruffleHog (segredos verificados) ----------
section "Segredos verificados — TruffleHog"
if have trufflehog; then
  log "Rodando trufflehog..."
  trufflehog filesystem "$REPO" --json --no-update > "$RAW/trufflehog.json" 2>/dev/null
  if [[ -s "$RAW/trufflehog.json" ]]; then
    # grep -c imprime "0" E sai 1 quando não há match; o `|| echo 0` antigo gerava "0\n0".
    verified=$(grep -c '"verified":true' "$RAW/trufflehog.json" 2>/dev/null || true)
    verified=${verified:-0}
    echo "**Segredos VERIFICADOS (ativos):** $verified — prioridade máxima." >> "$PRESCAN"
    echo "Detalhes em \`raw-scans/trufflehog.json\`." >> "$PRESCAN"
  else
    echo "Nenhuma saída." >> "$PRESCAN"
  fi
else
  skip trufflehog
fi

# ---------- 4. Trivy (SCA + IaC + secrets) ----------
section "SCA / IaC — Trivy"
if have trivy; then
  log "Rodando trivy fs..."
  trivy fs --scanners vuln,secret,misconfig --format json \
    --output "$RAW/trivy.json" "$REPO" >/dev/null 2>&1
  if have jq && [[ -f "$RAW/trivy.json" ]]; then
    crit=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length' "$RAW/trivy.json" 2>/dev/null || echo "?")
    high=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity=="HIGH")]     | length' "$RAW/trivy.json" 2>/dev/null || echo "?")
    misc=$(jq '[.Results[]?.Misconfigurations[]?]                                | length' "$RAW/trivy.json" 2>/dev/null || echo "?")
    echo "**Vulns dependências:** CRITICAL=$crit, HIGH=$high | **Misconfigs:** $misc" >> "$PRESCAN"; echo >> "$PRESCAN"
    echo "Top pacotes vulneráveis (CRITICAL/HIGH):" >> "$PRESCAN"; echo >> "$PRESCAN"
    jq -r '[.Results[]?.Vulnerabilities[]? | select(.Severity=="CRITICAL" or .Severity=="HIGH")]
           | .[] | "- \(.PkgName) \(.InstalledVersion) → \(.VulnerabilityID) (\(.Severity))"' \
      "$RAW/trivy.json" 2>/dev/null | sort -u | head -30 >> "$PRESCAN"
  fi
else
  skip trivy
fi

# ---------- 5. osv-scanner (fallback SCA) ----------
section "SCA — osv-scanner"
if have osv-scanner; then
  log "Rodando osv-scanner..."
  osv-scanner --format json --output "$RAW/osv.json" -r "$REPO" >/dev/null 2>&1
  if have jq && [[ -f "$RAW/osv.json" ]]; then
    n=$(jq '[.results[]?.packages[]?.vulnerabilities[]?] | length' "$RAW/osv.json" 2>/dev/null || echo "?")
    echo "**Vulnerabilidades OSV:** $n (detalhe em \`raw-scans/osv.json\`)." >> "$PRESCAN"
  fi
else
  skip osv-scanner
fi

# ---------- 6. Checkov (IaC) ----------
section "IaC — Checkov"
if have checkov; then
  if find "$REPO" \( -name "*.tf" -o -name "*.yaml" -o -name "*.yml" -o -name "Dockerfile" \) -not -path '*/node_modules/*' -print -quit | grep -q .; then
    log "Rodando checkov..."
    checkov -d "$REPO" -o json --compact > "$RAW/checkov.json" 2>/dev/null
    if have jq && [[ -f "$RAW/checkov.json" ]]; then
      failed=$(jq '.results.failed_checks | length' "$RAW/checkov.json" 2>/dev/null || echo "?")
      echo "**Checks de IaC falhos:** $failed" >> "$PRESCAN"; echo >> "$PRESCAN"
      jq -r '.results.failed_checks[]? | "- \(.check_id) \(.check_name) — `\(.file_path)`"' \
        "$RAW/checkov.json" 2>/dev/null | sort -u | head -25 >> "$PRESCAN"
    fi
  else
    echo "_Nenhum arquivo de IaC detectado — checkov pulado._" >> "$PRESCAN"
  fi
else
  skip checkov
fi

# ---------- 7. mcp-scan (escopo de tools MCP) ----------
section "MCP — mcp-scan"
if have mcp-scan; then
  # mcp-scan recebe ARQUIVOS de config MCP, não um diretório de repo.
  # Coleta por conteúdo ("mcpServers") e por nome de arquivo conhecido.
  MCP_CFGS=$( { grep -rlE '"mcpServers"' "$REPO" 2>/dev/null; \
               find "$REPO" \( -name "mcp.json" -o -name "claude_desktop_config.json" \) 2>/dev/null; \
             } | sort -u )
  if [[ -n "$MCP_CFGS" ]]; then
    log "Config MCP detectada, rodando mcp-scan..."
    printf '%s\n' "$MCP_CFGS" > "$RAW/mcp-configs.txt"
    # shellcheck disable=SC2086
    mcp-scan scan $MCP_CFGS > "$RAW/mcp-scan.txt" 2>&1 || true
    echo "Configs MCP em \`raw-scans/mcp-configs.txt\`; saída em \`raw-scans/mcp-scan.txt\` — revisar over-permission, escopo de tools e tool poisoning." >> "$PRESCAN"
  else
    echo "_Nenhuma config MCP detectada — mcp-scan pulado._" >> "$PRESCAN"
  fi
else
  skip mcp-scan
fi

# ---------- inventário rápido de stack ----------
section "Inventário rápido (fingerprint)"
{
  echo "Manifests/configs encontrados:"; echo
  find "$REPO" -maxdepth 4 \( \
    -name "package.json" -o -name "pnpm-lock.yaml" -o -name "yarn.lock" \
    -o -name "go.mod" -o -name "requirements.txt" -o -name "pyproject.toml" \
    -o -name "Pipfile" -o -name "composer.json" -o -name "Gemfile" \
    -o -name "pom.xml" -o -name "build.gradle" -o -name "*.gradle" \
    -o -name "Cargo.toml" -o -name "*.csproj" -o -name "mix.exs" \
    -o -name "pubspec.yaml" -o -name "Dockerfile" \
    -o -name "docker-compose*.yml" -o -name "*.tf" \) \
    -not -path '*/node_modules/*' -not -path '*/vendor/*' 2>/dev/null \
    | sed "s|$REPO|.|" | sort | sed 's/^/- /'
} >> "$PRESCAN"

# ---------- próximos passos ----------
section "Próximos passos (manual)"
cat >> "$PRESCAN" <<'NEXT'
1. Revisar `raw-scans/` e promover findings reais a rascunhos em `achados.yaml`.
2. Alimentar os prompts do **Pilar 2 (Analisar)** com os trechos de código sinalizados:
   - auth → `02-analisar/revisao-de-autenticacao-e-controle-de-acesso.md`
   - injection → `02-analisar/revisao-de-injection-e-execucao-arbitraria.md`
   - path-traversal/SSRF → `02-analisar/path-traversal-ssrf-e-validacao-de-entrada.md`
   - XSS/client-side → `02-analisar/revisao-de-xss-e-seguranca-client-side.md`
   - CORS/CSRF/headers → `02-analisar/revisao-de-cors-csrf-e-headers-de-seguranca.md`
   - segredos/config → `02-analisar/analise-de-segredos-e-configuracao-insegura.md`
   - cripto → `02-analisar/analise-de-criptografia-e-protecao-de-dados.md`
   - logging → `02-analisar/revisao-de-logging-auditoria-e-deteccao.md`
   - desserialização/race → `02-analisar/revisao-de-desserializacao-e-race-conditions.md`
   - IaC → `02-analisar/revisao-de-iac-gerado-por-ia.md`
   - MCP → `02-analisar/analise-de-configuracao-de-mcp-e-escopo-de-tools.md`
3. Marcar findings de scanner como `falso_positivo` quando triados; o que sobrar vira `rascunho`.
4. Seguir para o **Pilar 3 (Validar)** para confirmar explorabilidade (preencher `deriva_de`).
NEXT

log "Concluído. Resumo: $PRESCAN"
echo
echo "==> Pre-scan gerado em: $PRESCAN"
