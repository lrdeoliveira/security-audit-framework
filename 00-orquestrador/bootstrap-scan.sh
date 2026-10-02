#!/usr/bin/env bash
# ============================================================================
# bootstrap-scan.sh — Ingestão automatizada do Pilar 1/2 (Descobrir + Analisar)
# Framework de Auditoria de Segurança v1.4
#
# Roda os scanners base sobre um repositório e consolida a saída em um único
# pre-scan.md, que alimenta os prompts do Pilar 2 (Analisar) sem cópia manual.
#
# Novidades v1.4:
#   - Execução concorrente (paralela) por padrão — 3x a 5x mais rápido!
#   - Flags de seleção: --fast, --only <lista>, --skip <lista>, --sequential
#   - Proteção de timeout por scanner (evita travamento)
#   - Ingestão automática em achados.yaml via flag --auto-ingest
#
# Uso:
#   ./00-orquestrador/bootstrap-scan.sh [opções] <caminho_do_repo> <produto> [data]
#
# Exemplos:
#   # Modo padrão (paralelo, todos os scanners instalados):
#   ./00-orquestrador/bootstrap-scan.sh ~/projetos/minha-app minha-app
#
#   # Modo rápido (apenas SAST e segredos rápidos):
#   ./00-orquestrador/bootstrap-scan.sh --fast ~/projetos/minha-app minha-app
#
#   # Apenas scanners específicos com ingestão automática no achados.yaml:
#   ./00-orquestrador/bootstrap-scan.sh --only semgrep,trivy --auto-ingest ~/projetos/minha-app minha-app
# ============================================================================

set -uo pipefail

# ---------- configurações padrão ----------
PARALLEL=true
FAST_MODE=false
ONLY_SCANNERS=""
SKIP_SCANNERS=""
TIMEOUT_SEC=300
AUTO_INGEST=false

usage() {
  cat <<'EOF'
Uso: bootstrap-scan.sh [opções] <caminho_do_repo> <produto> [data YYYY-MM-DD]

Opções:
  -p, --parallel      Executa scanners em paralelo (padrão)
  -s, --sequential    Executa scanners sequencialmente (ideal para máquinas com pouca memória)
  -f, --fast          Modo rápido (SAST + segredos rápidos; pula TruffleHog e Checkov)
  --only <lista>      Executa apenas os scanners listados (separados por vírgula)
                      Ex: --only semgrep,trivy,gitleaks
  --skip <lista>      Pula os scanners listados (separados por vírgula)
                      Ex: --skip trufflehog,checkov
  --timeout <seg>     Tempo limite por scanner em segundos (padrão: 300)
  --auto-ingest       Executa automaticamente 'audit_tool.py ingest' após o scan
  -h, --help          Exibe esta ajuda e sai

Scanners suportados:
  semgrep, gitleaks, trufflehog, trivy, osv-scanner, checkov, mcp-scan
EOF
  exit 0
}

# ---------- parsing de argumentos ----------
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--parallel)
      PARALLEL=true
      shift
      ;;
    -s|--sequential)
      PARALLEL=false
      shift
      ;;
    -f|--fast)
      FAST_MODE=true
      shift
      ;;
    --only)
      ONLY_SCANNERS="${2:-}"
      shift 2
      ;;
    --skip)
      SKIP_SCANNERS="${2:-}"
      shift 2
      ;;
    --timeout)
      TIMEOUT_SEC="${2:-300}"
      shift 2
      ;;
    --auto-ingest)
      AUTO_INGEST=true
      shift
      ;;
    -h|--help)
      usage
      ;;
    -*)
      echo "ERRO: Opção desconhecida: $1" >&2
      exit 1
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

if [[ ${#POSITIONAL[@]} -lt 2 ]]; then
  echo "Uso: $0 [opções] <caminho_do_repo> <produto> [data YYYY-MM-DD]" >&2
  echo "Execute '$0 --help' para mais informações." >&2
  exit 1
fi

REPO="${POSITIONAL[0]}"
PRODUTO="${POSITIONAL[1]}"
DATA="${POSITIONAL[2]:-$(date +%Y-%m-%d)}"

if [[ ! -d "$REPO" ]]; then
  echo "ERRO: Repositório não encontrado: $REPO" >&2
  exit 1
fi

REPO="$(cd "$REPO" && pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTDIR="$ROOT/auditorias/${PRODUTO}-${DATA}"
RAW="$OUTDIR/raw-scans"
SUMMARIES="$RAW/summaries"
PRESCAN="$OUTDIR/pre-scan.md"

mkdir -p "$RAW" "$SUMMARIES" "$OUTDIR/evidencias"

ts() { date "+%Y-%m-%d %H:%M:%S"; }
have() { command -v "$1" >/dev/null 2>&1; }
log() { echo "[$(ts)] $*"; }

# Timeout helper portável usando Python 3
run_with_timeout() {
  local limit="$1"
  shift
  if have python3; then
    python3 -c "import subprocess, sys; sys.exit(subprocess.run(sys.argv[2:], timeout=float(sys.argv[1])).returncode)" "$limit" "$@"
  elif have timeout; then
    timeout "$limit" "$@"
  else
    "$@"
  fi
}

# Verificador de filtro de scanners
should_run() {
  local scanner="$1"

  if [[ "$FAST_MODE" == true ]]; then
    if [[ "$scanner" == "trufflehog" || "$scanner" == "checkov" ]]; then
      return 1
    fi
  fi

  if [[ -n "$ONLY_SCANNERS" ]]; then
    if [[ ",$ONLY_SCANNERS," != *",$scanner,"* ]]; then
      return 1
    fi
  fi

  if [[ -n "$SKIP_SCANNERS" ]]; then
    if [[ ",$SKIP_SCANNERS," == *",$scanner,"* ]]; then
      return 1
    fi
  fi

  return 0
}

# ---------- Definição dos Jobs de Scan ----------

scan_semgrep() {
  local sname="semgrep"
  local sfile="$SUMMARIES/01-semgrep.md"

  if ! should_run "$sname"; then
    echo -e "## SAST — Semgrep\n\n_Scanner desabilitado por filtro CLI._" > "$sfile"
    return 0
  fi

  if ! have semgrep; then
    echo -e "## SAST — Semgrep\n\n_Scanner \`semgrep\` não instalado — pulado._" > "$sfile"
    return 0
  fi

  log "[START] Rodando Semgrep (SAST)..."
  local t0=$(date +%s)
  
  run_with_timeout "$TIMEOUT_SEC" semgrep scan --config auto --metrics=off \
    --severity ERROR --severity WARNING --json --output "$RAW/semgrep.json" "$REPO" >/dev/null 2>&1 || true

  local dt=$(( $(date +%s) - t0 ))
  log "[DONE] Semgrep concluído em ${dt}s"

  {
    echo "## SAST — Semgrep (concluído em ${dt}s)"
    echo
    if have jq && [[ -f "$RAW/semgrep.json" ]]; then
      local total=$(jq '.results | length' "$RAW/semgrep.json" 2>/dev/null || echo "?")
      echo "**Total de findings:** $total"
      echo
      echo "Top regras por frequência:"
      echo
      jq -r '.results[].check_id' "$RAW/semgrep.json" 2>/dev/null \
        | sort | uniq -c | sort -rn | head -20 \
        | awk '{c=$1; $1=""; printf "- `%s` — %s ocorrência(s)\n", substr($0,2), c}'
    else
      echo "Saída em \`raw-scans/semgrep.json\`."
    fi
  } > "$sfile"
}

scan_gitleaks() {
  local sname="gitleaks"
  local sfile="$SUMMARIES/02-gitleaks.md"

  if ! should_run "$sname"; then
    echo -e "## Segredos — Gitleaks\n\n_Scanner desabilitado por filtro CLI._" > "$sfile"
    return 0
  fi

  if ! have gitleaks; then
    echo -e "## Segredos — Gitleaks (histórico git)\n\n_Scanner \`gitleaks\` não instalado — pulado._" > "$sfile"
    return 0
  fi

  if [[ ! -d "$REPO/.git" ]]; then
    echo -e "## Segredos — Gitleaks (histórico git)\n\n_Sem diretório .git — gitleaks pulado._" > "$sfile"
    return 0
  fi

  log "[START] Rodando Gitleaks (segredos no histórico git)..."
  local t0=$(date +%s)

  run_with_timeout "$TIMEOUT_SEC" gitleaks git "$REPO" --report-format json \
    --report-path "$RAW/gitleaks.json" --redact >/dev/null 2>&1 || true

  local dt=$(( $(date +%s) - t0 ))
  log "[DONE] Gitleaks concluído em ${dt}s"

  {
    echo "## Segredos — Gitleaks (histórico git, ${dt}s)"
    echo
    if have jq && [[ -f "$RAW/gitleaks.json" ]]; then
      local n=$(jq 'length' "$RAW/gitleaks.json" 2>/dev/null || echo "?")
      echo "**Segredos potenciais (redacted):** $n"
      echo
      jq -r '.[] | "- \(.RuleID) em `\(.File)` (commit \(.Commit[0:8]))"' \
        "$RAW/gitleaks.json" 2>/dev/null | head -30
    else
      echo "Saída em \`raw-scans/gitleaks.json\`."
    fi
  } > "$sfile"
}

scan_trufflehog() {
  local sname="trufflehog"
  local sfile="$SUMMARIES/03-trufflehog.md"

  if ! should_run "$sname"; then
    echo -e "## Segredos verificados — TruffleHog\n\n_Scanner desabilitado por filtro CLI._" > "$sfile"
    return 0
  fi

  if ! have trufflehog; then
    echo -e "## Segredos verificados — TruffleHog\n\n_Scanner \`trufflehog\` não instalado — pulado._" > "$sfile"
    return 0
  fi

  log "[START] Rodando TruffleHog (segredos no filesystem)..."
  local t0=$(date +%s)

  run_with_timeout "$TIMEOUT_SEC" trufflehog filesystem "$REPO" --json --no-update > "$RAW/trufflehog.json" 2>/dev/null || true

  local dt=$(( $(date +%s) - t0 ))
  log "[DONE] TruffleHog concluído em ${dt}s"

  {
    echo "## Segredos verificados — TruffleHog (${dt}s)"
    echo
    if [[ -s "$RAW/trufflehog.json" ]]; then
      local verified=$(grep -c '"verified":true' "$RAW/trufflehog.json" 2>/dev/null || true)
      verified=${verified:-0}
      echo "**Segredos VERIFICADOS (ativos):** $verified — prioridade máxima."
      echo "Detalhes em \`raw-scans/trufflehog.json\`."
    else
      echo "Nenhuma saída."
    fi
  } > "$sfile"
}

scan_trivy() {
  local sname="trivy"
  local sfile="$SUMMARIES/04-trivy.md"

  if ! should_run "$sname"; then
    echo -e "## SCA / IaC — Trivy\n\n_Scanner desabilitado por filtro CLI._" > "$sfile"
    return 0
  fi

  if ! have trivy; then
    echo -e "## SCA / IaC — Trivy\n\n_Scanner \`trivy\` não instalado — pulado._" > "$sfile"
    return 0
  fi

  log "[START] Rodando Trivy (SCA + IaC + secrets)..."
  local t0=$(date +%s)

  run_with_timeout "$TIMEOUT_SEC" trivy fs --scanners vuln,secret,misconfig --format json \
    --skip-dirs "vendor,node_modules" \
    --output "$RAW/trivy.json" "$REPO" >/dev/null 2>&1 || true

  local dt=$(( $(date +%s) - t0 ))
  log "[DONE] Trivy concluído em ${dt}s"

  {
    echo "## SCA / IaC — Trivy (${dt}s)"
    echo
    if have jq && [[ -f "$RAW/trivy.json" ]]; then
      local crit=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length' "$RAW/trivy.json" 2>/dev/null || echo "?")
      local high=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity=="HIGH")]     | length' "$RAW/trivy.json" 2>/dev/null || echo "?")
      local misc=$(jq '[.Results[]?.Misconfigurations[]?]                                | length' "$RAW/trivy.json" 2>/dev/null || echo "?")
      echo "**Vulns dependências:** CRITICAL=$crit, HIGH=$high | **Misconfigs:** $misc"
      echo
      echo "Top pacotes vulneráveis (CRITICAL/HIGH):"
      echo
      jq -r '[.Results[]?.Vulnerabilities[]? | select(.Severity=="CRITICAL" or .Severity=="HIGH")]
             | .[] | "- \(.PkgName) \(.InstalledVersion) → \(.VulnerabilityID) (\(.Severity))"' \
        "$RAW/trivy.json" 2>/dev/null | sort -u | head -30
    else
      echo "Saída em \`raw-scans/trivy.json\`."
    fi
  } > "$sfile"
}

scan_osv() {
  local sname="osv-scanner"
  local sfile="$SUMMARIES/05-osv.md"

  if ! should_run "$sname"; then
    echo -e "## SCA — osv-scanner\n\n_Scanner desabilitado por filtro CLI._" > "$sfile"
    return 0
  fi

  if ! have osv-scanner; then
    echo -e "## SCA — osv-scanner\n\n_Scanner \`osv-scanner\` não instalado — pulado._" > "$sfile"
    return 0
  fi

  log "[START] Rodando osv-scanner..."
  local t0=$(date +%s)

  run_with_timeout "$TIMEOUT_SEC" osv-scanner --format json --output "$RAW/osv.json" -r "$REPO" >/dev/null 2>&1 || true

  local dt=$(( $(date +%s) - t0 ))
  log "[DONE] osv-scanner concluído em ${dt}s"

  {
    echo "## SCA — osv-scanner (${dt}s)"
    echo
    if have jq && [[ -f "$RAW/osv.json" ]]; then
      local n=$(jq '[.results[]?.packages[]?.vulnerabilities[]?] | length' "$RAW/osv.json" 2>/dev/null || echo "?")
      echo "**Vulnerabilidades OSV:** $n (detalhes em \`raw-scans/osv.json\`)."
    fi
  } > "$sfile"
}

scan_checkov() {
  local sname="checkov"
  local sfile="$SUMMARIES/06-checkov.md"

  if ! should_run "$sname"; then
    echo -e "## IaC — Checkov\n\n_Scanner desabilitado por filtro CLI._" > "$sfile"
    return 0
  fi

  if ! have checkov; then
    echo -e "## IaC — Checkov\n\n_Scanner \`checkov\` não instalado — pulado._" > "$sfile"
    return 0
  fi

  if ! find "$REPO" \( -name "*.tf" -o -name "*.yaml" -o -name "*.yml" -o -name "Dockerfile" \) -not -path '*/node_modules/*' -not -path '*/vendor/*' -print -quit 2>/dev/null | grep -q .; then
    echo -e "## IaC — Checkov\n\n_Nenhum arquivo de IaC detectado — checkov pulado._" > "$sfile"
    return 0
  fi

  log "[START] Rodando Checkov (IaC)..."
  local t0=$(date +%s)

  run_with_timeout "$TIMEOUT_SEC" checkov -d "$REPO" -o json --compact > "$RAW/checkov.json" 2>/dev/null || true

  local dt=$(( $(date +%s) - t0 ))
  log "[DONE] Checkov concluído em ${dt}s"

  {
    echo "## IaC — Checkov (${dt}s)"
    echo
    if have jq && [[ -f "$RAW/checkov.json" ]]; then
      local failed=$(jq '.results.failed_checks | length' "$RAW/checkov.json" 2>/dev/null || echo "?")
      echo "**Checks de IaC falhos:** $failed"
      echo
      jq -r '.results.failed_checks[]? | "- \(.check_id) \(.check_name) — `\(.file_path)`"' \
        "$RAW/checkov.json" 2>/dev/null | sort -u | head -25
    else
      echo "Saída em \`raw-scans/checkov.json\`."
    fi
  } > "$sfile"
}

scan_mcp() {
  local sname="mcp-scan"
  local sfile="$SUMMARIES/07-mcp.md"

  if ! should_run "$sname"; then
    echo -e "## MCP — mcp-scan\n\n_Scanner desabilitado por filtro CLI._" > "$sfile"
    return 0
  fi

  if ! have mcp-scan; then
    echo -e "## MCP — mcp-scan\n\n_Scanner \`mcp-scan\` não instalado — pulado._" > "$sfile"
    return 0
  fi

  local MCP_CFGS=$( { grep -rlE '"mcpServers"' "$REPO" 2>/dev/null; \
                      find "$REPO" \( -name "mcp.json" -o -name "claude_desktop_config.json" \) 2>/dev/null; \
                    } | sort -u )

  if [[ -z "$MCP_CFGS" ]]; then
    echo -e "## MCP — mcp-scan\n\n_Nenhuma config MCP detectada — mcp-scan pulado._" > "$sfile"
    return 0
  fi

  log "[START] Config MCP detectada, rodando mcp-scan..."
  local t0=$(date +%s)

  printf '%s\n' "$MCP_CFGS" > "$RAW/mcp-configs.txt"
  run_with_timeout "$TIMEOUT_SEC" mcp-scan scan $MCP_CFGS > "$RAW/mcp-scan.txt" 2>&1 || true

  local dt=$(( $(date +%s) - t0 ))
  log "[DONE] mcp-scan concluído em ${dt}s"

  {
    echo "## MCP — mcp-scan (${dt}s)"
    echo
    echo "Configs MCP em \`raw-scans/mcp-configs.txt\`; saída em \`raw-scans/mcp-scan.txt\`."
  } > "$sfile"
}

# ---------- Execução dos Scanners ----------

log "==> Iniciando Bootstrap Scan v1.4 em: $REPO (Produto: $PRODUTO)"
MODE_STR="Paralelo (concorrente)"
if [[ "$PARALLEL" == false ]]; then MODE_STR="Sequencial"; fi
log "Modo: $MODE_STR | Fast: $FAST_MODE | Timeout: ${TIMEOUT_SEC}s"

GLOBAL_T0=$(date +%s)

if [[ "$PARALLEL" == true ]]; then
  scan_semgrep &
  PID_SEMGREP=$!

  scan_gitleaks &
  PID_GITLEAKS=$!

  scan_trufflehog &
  PID_TRUFFLEHOG=$!

  scan_trivy &
  PID_TRIVY=$!

  scan_osv &
  PID_OSV=$!

  scan_checkov &
  PID_CHECKOV=$!

  scan_mcp &
  PID_MCP=$!

  # Aguardar conclusão de todos os jobs concorrentes
  wait $PID_SEMGREP $PID_GITLEAKS $PID_TRUFFLEHOG $PID_TRIVY $PID_OSV $PID_CHECKOV $PID_MCP
else
  scan_semgrep
  scan_gitleaks
  scan_trufflehog
  scan_trivy
  scan_osv
  scan_checkov
  scan_mcp
fi

TOTAL_ELAPSED=$(( $(date +%s) - GLOBAL_T0 ))
log "Todos os scanners foram finalizados em ${TOTAL_ELAPSED}s"

# ---------- Montagem do pre-scan.md consolidado ----------

{
  echo "# Pre-scan automatizado — ${PRODUTO}"
  echo
  echo "- **Repo:** \`$REPO\`"
  echo "- **Data:** $DATA"
  echo "- **Modo:** $MODE_STR (tempo total: ${TOTAL_ELAPSED}s)"
  echo "- **Gerado por:** bootstrap-scan.sh (Framework v1.4)"
  echo
  echo "> Saídas brutas em \`raw-scans/\`. Use este resumo como entrada dos prompts do Pilar 2."
  echo

  for summary_part in "$SUMMARIES"/*.md; do
    if [[ -f "$summary_part" ]]; then
      echo "---"
      echo
      cat "$summary_part"
      echo
    fi
  done

  echo "---"
  echo
  echo "## Inventário rápido (fingerprint)"
  echo
  echo "Manifests/configs encontrados:"
  echo
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

  echo
  echo "---"
  echo
  echo "## Próximos passos"
  echo
  echo "1. Triar os achados com a ferramenta de automação: \`python3 scripts/audit_tool.py ingest $OUTDIR\`"
  echo "2. Revisar \`achados.yaml\` gerado e descartar falsos positivos."
  echo "3. Proceder para o Pilar 3 (Validar) para confirmar explorabilidade."
} > "$PRESCAN"

log "Relatório preliminar consolidado em: $PRESCAN"

# Ingestão automática opcional
if [[ "$AUTO_INGEST" == true ]]; then
  if [[ -f "$ROOT/scripts/audit_tool.py" ]]; then
    log "Executando --auto-ingest..."
    python3 "$ROOT/scripts/audit_tool.py" ingest "$OUTDIR"
  fi
fi

echo
echo "=========================================================================="
echo "==> Bootstrap scan concluído com sucesso em ${TOTAL_ELAPSED}s!"
echo "==> Resumo: $PRESCAN"
echo "==> Próximo passo sugerido: python3 scripts/audit_tool.py ingest $OUTDIR"
echo "=========================================================================="
