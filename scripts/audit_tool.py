#!/usr/bin/env python3
"""
audit_tool.py — Ferramenta unificada de automação do Security Audit Framework
v1.4 — Ingestão automática, validação de schema, geração de laudo e seleção de prompts.

Comandos:
  ingest    Ingere saídas brutas de scanners (semgrep, trivy, gitleaks, trufflehog, checkov, osv)
            e gera rascunhos estruturados em achados.yaml.
  validate  Valida o arquivo achados.yaml contra o schema do framework (regras, enums, CVSS, coerência).
  report    Compila achados.yaml no relatório final relatorio-final.md com métricas, matriz e cards.
  select    Filtra e retorna prompts recomendados para o stack/contexto do alvo (economiza tokens).
  stats     Exibe um resumo tabular rápido dos achados no terminal.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    print("ERRO: PyYAML não está instalado. Instale com: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ==============================================================================
# Constantes e Vocabulário Controlado (AUDITORIA.md v1.4)
# ==============================================================================

VALID_SEVERITIES = {"critico", "alto", "medio", "baixo", "info"}
VALID_STATUS = {"rascunho", "confirmado", "falso_positivo", "corrigido"}
VALID_PILARES = {"descobrir", "analisar", "validar", "entregar"}
VALID_SUBPILARES = {"dast", "red-team", "ia", None}
VALID_RETESTE = {"pendente", "aprovado", "reprovado"}

SEVERITY_ORDER = {
    "critico": 0,
    "alto": 1,
    "medio": 2,
    "baixo": 3,
    "info": 4,
}

FRAMEWORK_VERSION = "1.4"


# ==============================================================================
# Utilitários de Formatação de Terminal (ANSI)
# ==============================================================================

class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def colorize(text: str, color: str) -> str:
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.RESET}"
    return text


def severity_color(sev: str) -> str:
    m = {
        "critico": Colors.RED + Colors.BOLD,
        "alto": Colors.RED,
        "medio": Colors.YELLOW,
        "baixo": Colors.BLUE,
        "info": Colors.CYAN,
    }
    return m.get(sev.lower(), "")


# ==============================================================================
# Modelos de Dados
# ==============================================================================

@dataclass
class Finding:
    id: str
    titulo: str
    severidade: str
    cvss: str
    owasp: str
    cwe: str
    pilar: str
    subpilar: Optional[str] = None
    status: str = "rascunho"
    prompt_origem: str = ""
    deriva_de: Optional[str] = None
    localizacao: str = ""
    descricao: str = ""
    poc: str = ""
    impacto: str = ""
    remediacao: str = ""
    referencias: List[str] = field(default_factory=list)
    evidencias: str = ""
    data_descoberta: str = field(default_factory=lambda: date.today().isoformat())
    data_correcao: Optional[str] = None
    reteste: str = "pendente"
    conformidade: Dict[str, Optional[str]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "id": self.id,
            "titulo": self.titulo,
            "severidade": self.severidade,
            "cvss": self.cvss,
            "owasp": self.owasp,
            "cwe": self.cwe,
            "pilar": self.pilar,
            "subpilar": self.subpilar,
            "status": self.status,
            "prompt_origem": self.prompt_origem,
            "deriva_de": self.deriva_de,
            "conformidade": self.conformidade or {
                "lgpd": None,
                "gdpr": None,
                "soc2": None,
                "iso27001": None,
                "asvs": None,
                "pci_dss": None,
                "nist_csf": None,
                "cis": None,
            },
            "localizacao": self.localizacao,
            "descricao": self.descricao.strip(),
            "poc": self.poc.strip(),
            "impacto": self.impacto.strip(),
            "remediacao": self.remediacao.strip(),
            "referencias": self.referencias,
            "evidencias": self.evidencias,
            "data_descoberta": self.data_descoberta,
            "data_correcao": self.data_correcao,
            "reteste": self.reteste,
        }
        return d


# ==============================================================================
# Parsers de Scanners (Ingestão Automatizada)
# ==============================================================================

def map_semgrep_to_finding(result: Dict[str, Any], next_id: int) -> Finding:
    check_id = result.get("check_id", "semgrep.finding")
    path = result.get("path", "")
    line = result.get("start", {}).get("line", 1)
    extra = result.get("extra", {})
    msg = extra.get("message", "").strip()
    semgrep_sev = extra.get("severity", "WARNING").upper()
    metadata = extra.get("metadata", {})

    # Mapear severidade
    if semgrep_sev == "ERROR":
        sev = "alto"
    elif semgrep_sev == "WARNING":
        sev = "medio"
    else:
        sev = "baixo"

    # Mapear CWE e OWASP
    cwe_raw = metadata.get("cwe", [])
    if isinstance(cwe_raw, list) and cwe_raw:
        cwe_str = cwe_raw[0]
        cwe_match = re.search(r"CWE-\d+", cwe_str)
        cwe = cwe_match.group(0) if cwe_match else "CWE-20"
    elif isinstance(cwe_raw, str):
        cwe_match = re.search(r"CWE-\d+", cwe_raw)
        cwe = cwe_match.group(0) if cwe_match else "CWE-20"
    else:
        cwe = "CWE-20"

    owasp_raw = metadata.get("owasp", [])
    if isinstance(owasp_raw, list) and owasp_raw:
        owasp = owasp_raw[0]
    elif isinstance(owasp_raw, str):
        owasp = owasp_raw
    else:
        owasp = "A05:2021 - Security Misconfiguration"

    # Prompts de origem aproximados
    prompt_origem = "02-analisar/revisao-de-injection-e-execucao-arbitraria.md"
    cid_lower = check_id.lower()
    if any(k in cid_lower for k in ["secret", "key", "token", "password"]):
        prompt_origem = "02-analisar/analise-de-segredos-e-configuracao-insegura.md"
    elif any(k in cid_lower for k in ["auth", "jwt", "session", "permission", "rbac"]):
        prompt_origem = "02-analisar/revisao-de-autenticacao-e-controle-de-acesso.md"
    elif any(k in cid_lower for k in ["xss", "dangerously", "innerhtml"]):
        prompt_origem = "02-analisar/revisao-de-xss-e-seguranca-client-side.md"
    elif any(k in cid_lower for k in ["ssrf", "traversal", "urllib", "requests"]):
        prompt_origem = "02-analisar/path-traversal-ssrf-e-validacao-de-entrada.md"
    elif any(k in cid_lower for k in ["cors", "csrf", "header"]):
        prompt_origem = "02-analisar/revisao-de-cors-csrf-e-headers-de-seguranca.md"
    elif any(k in cid_lower for k in ["crypto", "des", "md5", "sha1", "cipher", "tls"]):
        prompt_origem = "02-analisar/analise-de-criptografia-e-protecao-de-dados.md"

    title = f"[Semgrep] {check_id.split('.')[-1].replace('-', ' ').title()}"
    loc = f"{path}:{line}"

    refs = []
    if "references" in metadata and isinstance(metadata["references"], list):
        refs = metadata["references"][:3]

    return Finding(
        id=f"AUD-{next_id:03d}",
        titulo=title,
        severidade=sev,
        cvss="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N (5.3)" if sev == "medio" else "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N (8.7)",
        owasp=owasp,
        cwe=cwe,
        pilar="analisar",
        subpilar=None,
        status="rascunho",
        prompt_origem=prompt_origem,
        localizacao=loc,
        descricao=f"Regra Semgrep `{check_id}`:\n{msg}",
        poc=f"# Reprodução estática:\nsemgrep scan --config auto --severity {semgrep_sev} {path}",
        impacto=f"Violação de segurança detectada pela regra {check_id}.",
        remediacao=f"Revisar o trecho em {loc} e implementar as práticas recomendadas pelo CWE {cwe}.",
        referencias=refs,
    )


def map_gitleaks_to_finding(result: Dict[str, Any], next_id: int) -> Finding:
    rule = result.get("RuleID", "Secret")
    file_path = result.get("File", "")
    line = result.get("StartLine", 1)
    commit = result.get("Commit", "")[:8]
    secret_redacted = result.get("Secret", "[REDACTED]")

    return Finding(
        id=f"AUD-{next_id:03d}",
        titulo=f"[Gitleaks] Possível segredo exposto no histórico: {rule}",
        severidade="alto",
        cvss="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N (8.7)",
        owasp="A02:2021 - Security Misconfiguration",
        cwe="CWE-798",
        pilar="analisar",
        subpilar=None,
        status="rascunho",
        prompt_origem="02-analisar/analise-de-segredos-e-configuracao-insegura.md",
        localizacao=f"{file_path}:{line} (commit {commit})",
        descricao=f"Gitleaks detectou correspondência com a regra `{rule}` no commit `{commit}`.\nValor aproximado: `{secret_redacted}`",
        poc=f"git show {commit}:{file_path}",
        impacto="Exposição de credenciais ou chaves secretas pode permitir acesso indevido a serviços e infraestrutura.",
        remediacao="1. Revogar e rotacionar o segredo imediatamente.\n2. Remover o segredo do histórico git com bfg-repo-cleaner ou git-filter-repo.\n3. Configurar pré-commit hooks com gitleaks.",
        referencias=["https://cwe.mitre.org/data/definitions/798.html"],
    )


def map_trufflehog_to_finding(result: Dict[str, Any], next_id: int) -> Finding:
    detector = result.get("DetectorName", "Secret")
    verified = result.get("Verified", False)
    src_meta = result.get("SourceMetadata", {}).get("Data", {}).get("Filesystem", {})
    file_path = src_meta.get("file", "desconhecido")
    line = src_meta.get("line", 1)

    sev = "critico" if verified else "alto"
    title_suffix = "VERIFICADO E ATIVO" if verified else "detectado no filesystem"

    return Finding(
        id=f"AUD-{next_id:03d}",
        titulo=f"[TruffleHog] Segredo {detector} {title_suffix}",
        severidade=sev,
        cvss="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H (10.0)" if verified else "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N (8.7)",
        owasp="A02:2021 - Security Misconfiguration",
        cwe="CWE-798",
        pilar="analisar",
        subpilar=None,
        status="rascunho",
        prompt_origem="02-analisar/analise-de-segredos-e-configuracao-insegura.md",
        localizacao=f"{file_path}:{line}",
        descricao=f"TruffleHog detectou credencial do tipo `{detector}`.\nVerificado pelo provedor: **{verified}**.",
        poc=f"trufflehog filesystem --only-verified {file_path}",
        impacto="Comprometimento de credencial com acesso direto aos serviços associados.",
        remediacao="Revogar e rotacionar a chave no provedor imediatamente e mover para cofre de segredos (1Password, Vault, AWS Secrets Manager).",
        referencias=["https://cwe.mitre.org/data/definitions/798.html"],
    )


def map_trivy_vuln_to_finding(vuln: Dict[str, Any], target: str, next_id: int) -> Finding:
    vuln_id = vuln.get("VulnerabilityID", "VULN")
    pkg = vuln.get("PkgName", "unknown")
    installed = vuln.get("InstalledVersion", "")
    fixed = vuln.get("FixedVersion", "N/A")
    raw_sev = vuln.get("Severity", "MEDIUM").upper()
    title = vuln.get("Title") or f"Vulnerabilidade em dependência: {pkg}"
    desc = vuln.get("Description", "")
    cwe_list = vuln.get("CweIDs", [])
    cwe = cwe_list[0] if cwe_list else "CWE-1395"

    sev_map = {
        "CRITICAL": "critico",
        "HIGH": "alto",
        "MEDIUM": "medio",
        "LOW": "baixo",
    }
    sev = sev_map.get(raw_sev, "medio")

    cvss_str = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N (9.2)" if sev == "critico" else "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N (8.7)"

    return Finding(
        id=f"AUD-{next_id:03d}",
        titulo=f"[Trivy/SCA] {vuln_id} em {pkg} {installed}",
        severidade=sev,
        cvss=cvss_str,
        owasp="A06:2021 - Vulnerable and Outdated Components",
        cwe=cwe,
        pilar="descobrir",
        subpilar=None,
        status="rascunho",
        prompt_origem="01-descobrir/analise-de-package-manifest-e-dependencias.md",
        localizacao=f"{target} ({pkg}@{installed})",
        descricao=f"Dependência `{pkg}` ({installed}) possui vulnerabilidade conhecida `{vuln_id}`:\n{desc[:300]}...",
        poc=f"trivy fs --scanners vuln {target}",
        impacto=f"Exploração conhecida vinculada a {vuln_id}.",
        remediacao=f"Atualizar `{pkg}` para a versão corrigida `{fixed}` ou superior.",
        referencias=vuln.get("References", [])[:3] if vuln.get("References") else [f"https://nvd.nist.gov/vuln/detail/{vuln_id}"],
    )


def map_checkov_to_finding(check: Dict[str, Any], next_id: int) -> Finding:
    cid = check.get("check_id", "CKV")
    cname = check.get("check_name", "IaC Misconfiguration")
    fpath = check.get("file_path", "")
    lines = check.get("file_line_range", [1, 1])
    guideline = check.get("guideline", "")

    return Finding(
        id=f"AUD-{next_id:03d}",
        titulo=f"[Checkov/IaC] {cid}: {cname}",
        severidade="medio",
        cvss="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N (5.3)",
        owasp="A05:2021 - Security Misconfiguration",
        cwe="CWE-16",
        pilar="analisar",
        subpilar=None,
        status="rascunho",
        prompt_origem="02-analisar/revisao-de-iac-gerado-por-ia.md",
        localizacao=f"{fpath}:{lines[0]}",
        descricao=f"Checkov apontou falha de configuração `{cid}` ({cname}) no arquivo `{fpath}`.",
        poc=f"checkov -f {fpath} --check {cid}",
        impacto="Configuração insegura de infraestrutura como código (IaC/Docker/K8s).",
        remediacao=f"Adequar a configuração conforme diretriz: {guideline or 'Aplicar hardening recomendado pela documentação oficial.'}",
        referencias=[guideline] if guideline else [],
    )


# ==============================================================================
# Ingestão Central
# ==============================================================================

def ingest_raw_scans(
    audit_dir: Path,
    min_severity: str = "medio",
    skip_vendor: bool = True,
    dry_run: bool = False,
) -> List[Finding]:
    """Lê todos os JSONs em audit_dir/raw-scans e retorna uma lista de Findings deduplicados."""
    raw_dir = audit_dir / "raw-scans"
    if not raw_dir.is_dir():
        print(f"ERRO: pasta raw-scans não encontrada em {audit_dir}", file=sys.stderr)
        return []

    min_sev_rank = SEVERITY_ORDER.get(min_severity.lower(), 2)

    findings: List[Finding] = []
    seen_keys: Set[str] = set()
    next_id = 1

    # Carregar achados já existentes se houver achados.yaml
    achados_file = audit_dir / "achados.yaml"
    existing_meta: Dict[str, Any] = {}
    if achados_file.is_file():
        try:
            with open(achados_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                existing_meta = data.get("meta", {})
                for item in data.get("achados", []):
                    # Guardar chave de deduplicação
                    loc = item.get("localizacao", "")
                    title = item.get("titulo", "")
                    seen_keys.add(f"{title}|{loc}")
                    # Determinar maior ID numérico
                    m = re.search(r"AUD-(\d+)", str(item.get("id", "")))
                    if m:
                        next_id = max(next_id, int(m.group(1)) + 1)
        except Exception as e:
            print(f"AVISO: não foi possível ler achados.yaml existente: {e}", file=sys.stderr)

    # 1. Semgrep
    semgrep_file = raw_dir / "semgrep.json"
    if semgrep_file.is_file():
        try:
            with open(semgrep_file, "r", encoding="utf-8") as f:
                sg_data = json.load(f)
                for res in sg_data.get("results", []):
                    path = res.get("path", "")
                    if skip_vendor and any(v in path for v in ["vendor/", "node_modules/", ".git/"]):
                        continue
                    finding = map_semgrep_to_finding(res, next_id)
                    key = f"{finding.titulo}|{finding.localizacao}"
                    if key in seen_keys:
                        continue
                    if SEVERITY_ORDER.get(finding.severidade, 4) <= min_sev_rank:
                        findings.append(finding)
                        seen_keys.add(key)
                        next_id += 1
        except Exception as e:
            print(f"AVISO: falha ao ler semgrep.json: {e}", file=sys.stderr)

    # 2. Gitleaks
    gitleaks_file = raw_dir / "gitleaks.json"
    if gitleaks_file.is_file():
        try:
            with open(gitleaks_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content and content != "[]":
                    gl_data = json.loads(content)
                    if isinstance(gl_data, list):
                        for item in gl_data:
                            fpath = item.get("File", "")
                            if skip_vendor and any(v in fpath for v in ["vendor/", "node_modules/"]):
                                continue
                            finding = map_gitleaks_to_finding(item, next_id)
                            key = f"{finding.titulo}|{finding.localizacao}"
                            if key in seen_keys:
                                continue
                            if SEVERITY_ORDER.get(finding.severidade, 4) <= min_sev_rank:
                                findings.append(finding)
                                seen_keys.add(key)
                                next_id += 1
        except Exception as e:
            print(f"AVISO: falha ao ler gitleaks.json: {e}", file=sys.stderr)

    # 3. TruffleHog (NDJSON)
    th_file = raw_dir / "trufflehog.json"
    if th_file.is_file():
        try:
            with open(th_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        fpath = obj.get("SourceMetadata", {}).get("Data", {}).get("Filesystem", {}).get("file", "")
                        if skip_vendor and any(v in fpath for v in ["vendor/", "node_modules/"]):
                            continue
                        finding = map_trufflehog_to_finding(obj, next_id)
                        key = f"{finding.titulo}|{finding.localizacao}"
                        if key in seen_keys:
                            continue
                        if SEVERITY_ORDER.get(finding.severidade, 4) <= min_sev_rank:
                            findings.append(finding)
                            seen_keys.add(key)
                            next_id += 1
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"AVISO: falha ao ler trufflehog.json: {e}", file=sys.stderr)

    # 4. Trivy
    trivy_file = raw_dir / "trivy.json"
    if trivy_file.is_file():
        try:
            with open(trivy_file, "r", encoding="utf-8") as f:
                tr_data = json.load(f)
                for res in tr_data.get("Results", []):
                    target = res.get("Target", "")
                    if skip_vendor and any(v in target for v in ["vendor/", "node_modules/"]):
                        continue
                    for v in res.get("Vulnerabilities", []):
                        finding = map_trivy_vuln_to_finding(v, target, next_id)
                        key = f"{finding.titulo}|{finding.localizacao}"
                        if key in seen_keys:
                            continue
                        if SEVERITY_ORDER.get(finding.severidade, 4) <= min_sev_rank:
                            findings.append(finding)
                            seen_keys.add(key)
                            next_id += 1
        except Exception as e:
            print(f"AVISO: falha ao ler trivy.json: {e}", file=sys.stderr)

    # 5. Checkov
    checkov_file = raw_dir / "checkov.json"
    if checkov_file.is_file():
        try:
            with open(checkov_file, "r", encoding="utf-8") as f:
                ck_data = json.load(f)
                check_lists = []
                if isinstance(ck_data, list):
                    for sub in ck_data:
                        check_lists.extend(sub.get("results", {}).get("failed_checks", []))
                elif isinstance(ck_data, dict):
                    check_lists.extend(ck_data.get("results", {}).get("failed_checks", []))

                for check in check_lists:
                    fpath = check.get("file_path", "")
                    if skip_vendor and any(v in fpath for v in ["vendor/", "node_modules/"]):
                        continue
                    finding = map_checkov_to_finding(check, next_id)
                    key = f"{finding.titulo}|{finding.localizacao}"
                    if key in seen_keys:
                        continue
                    if SEVERITY_ORDER.get(finding.severidade, 4) <= min_sev_rank:
                        findings.append(finding)
                        seen_keys.add(key)
                        next_id += 1
        except Exception as e:
            print(f"AVISO: falha ao ler checkov.json: {e}", file=sys.stderr)

    return findings


def execute_ingest(args: argparse.Namespace) -> int:
    audit_dir = Path(args.audit_dir).resolve()
    print(colorize(f"==> Iniciando ingestão em: {audit_dir}", Colors.CYAN + Colors.BOLD))

    new_findings = ingest_raw_scans(
        audit_dir=audit_dir,
        min_severity=args.min_severity,
        skip_vendor=not args.include_vendor,
        dry_run=args.dry_run,
    )

    print(f"Total de novos achados pré-processados: {len(new_findings)}")
    for f in new_findings[:5]:
        print(f"  - [{colorize(f.severidade.upper(), severity_color(f.severidade))}] {f.id}: {f.titulo} ({f.localizacao})")
    if len(new_findings) > 5:
        print(f"  ... e mais {len(new_findings) - 5} achados.")

    if args.dry_run:
        print(colorize("\n[Dry-run] Nenhuma alteração gravada.", Colors.YELLOW))
        return 0

    achados_file = audit_dir / "achados.yaml"
    existing_data: Dict[str, Any] = {}
    if achados_file.is_file():
        with open(achados_file, "r", encoding="utf-8") as f:
            existing_data = yaml.safe_load(f) or {}

    meta = existing_data.get("meta") or {
        "produto": audit_dir.name.split("-")[0],
        "data_inicio": date.today().isoformat(),
        "data_fim": None,
        "auditor": "Security Audit Framework",
        "escopo": f"Scan automático de {audit_dir.name}",
        "versao_framework": FRAMEWORK_VERSION,
    }

    current_findings_dict = existing_data.get("achados") or []
    all_findings = current_findings_dict + [f.to_dict() for f in new_findings]

    # Recalcular resumo
    counts = {"total": len(all_findings), "critico": 0, "alto": 0, "medio": 0, "baixo": 0, "info": 0}
    for item in all_findings:
        sev = str(item.get("severidade", "info")).lower()
        if sev in counts:
            counts[sev] += 1

    cobertura = existing_data.get("cobertura") or {
        "endpoints_total": 0,
        "endpoints_testados": 0,
        "componentes_ia_total": 0,
        "componentes_ia_testados": 0,
        "observacao": "Ingestão automatizada de raw-scans.",
    }

    payload = {
        "meta": meta,
        "resumo": counts,
        "cobertura": cobertura,
        "achados": all_findings,
    }

    with open(achados_file, "w", encoding="utf-8") as f:
        yaml.dump(payload, f, sort_keys=False, allow_unicode=True, indent=2)

    print(colorize(f"\n[OK] achados.yaml atualizado com sucesso: {achados_file}", Colors.GREEN + Colors.BOLD))
    print(f"Estatísticas atuais: Crítico={counts['critico']}, Alto={counts['alto']}, Médio={counts['medio']}, Baixo={counts['baixo']}, Total={counts['total']}")
    return 0


# ==============================================================================
# Validação de Schema (Quality Gate)
# ==============================================================================

@dataclass
class ValidationError:
    finding_id: str
    field: str
    message: str
    is_warning: bool = False


def validate_audit_file(file_path: Path) -> Tuple[List[ValidationError], Dict[str, Any]]:
    errors: List[ValidationError] = []

    if not file_path.is_file():
        errors.append(ValidationError("Geral", "file", f"Arquivo não encontrado: {file_path}"))
        return errors, {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        errors.append(ValidationError("Geral", "yaml_syntax", f"Erro de sintaxe YAML: {e}"))
        return errors, {}

    if not isinstance(data, dict):
        errors.append(ValidationError("Geral", "root", "O arquivo deve ser um dicionário YAML"))
        return errors, {}

    # Validar meta
    meta = data.get("meta")
    if not isinstance(meta, dict):
        errors.append(ValidationError("meta", "meta", "Bloco 'meta' ausente ou inválido"))
    else:
        for req in ["produto", "data_inicio"]:
            if not meta.get(req):
                errors.append(ValidationError("meta", req, f"Campo obrigatório '{req}' ausente"))

    # Validar achados
    achados = data.get("achados", [])
    if not isinstance(achados, list):
        errors.append(ValidationError("achados", "achados", "Bloco 'achados' deve ser uma lista"))
        return errors, data

    known_ids: Set[str] = set()
    actual_counts = {"total": len(achados), "critico": 0, "alto": 0, "medio": 0, "baixo": 0, "info": 0}

    for idx, item in enumerate(achados):
        if not isinstance(item, dict):
            errors.append(ValidationError(f"item_{idx}", "item", "Item de achado deve ser um mapeamento"))
            continue

        fid = item.get("id") or f"SEM_ID_{idx}"
        if not re.match(r"^AUD-\d{3,}$", str(fid)):
            errors.append(ValidationError(str(fid), "id", f"ID deve seguir padrão AUD-NNN (recebido: '{fid}')"))
        if str(fid) in known_ids:
            errors.append(ValidationError(str(fid), "id", f"ID duplicado: '{fid}'"))
        known_ids.add(str(fid))

        # Severidade
        sev = str(item.get("severidade", "")).lower()
        if sev not in VALID_SEVERITIES:
            errors.append(ValidationError(str(fid), "severidade", f"Severidade inválida '{sev}'. Opções: {sorted(VALID_SEVERITIES)}"))
        else:
            actual_counts[sev] += 1

        # Status
        st = str(item.get("status", "")).lower()
        if st not in VALID_STATUS:
            errors.append(ValidationError(str(fid), "status", f"Status inválido '{st}'. Opções: {sorted(VALID_STATUS)}"))

        # Pilar
        pilar = str(item.get("pilar", "")).lower()
        if pilar not in VALID_PILARES:
            errors.append(ValidationError(str(fid), "pilar", f"Pilar inválido '{pilar}'. Opções: {sorted(VALID_PILARES)}"))

        # Subpilar
        sub = item.get("subpilar")
        if sub is not None and str(sub).lower() not in VALID_SUBPILARES:
            errors.append(ValidationError(str(fid), "subpilar", f"Subpilar inválido '{sub}'. Opções: dast, red-team, ia, null"))

        # Reteste
        ret = str(item.get("reteste", "")).lower()
        if ret not in VALID_RETESTE:
            errors.append(ValidationError(str(fid), "reteste", f"Reteste inválido '{ret}'. Opções: {sorted(VALID_RETESTE)}"))

        # Campos obrigatórios de conteúdo
        for req_field in ["titulo", "descricao", "remediacao", "localizacao"]:
            val = item.get(req_field)
            if not val or not str(val).strip():
                errors.append(ValidationError(str(fid), req_field, f"Campo '{req_field}' é obrigatório e está vazio"))

        # CVSS verificação de formato
        cvss = str(item.get("cvss", ""))
        if cvss and not re.search(r"CVSS:(?:4\.0|3\.[01])/", cvss):
            errors.append(ValidationError(str(fid), "cvss", f"Formato CVSS suspeito: '{cvss}'. Esperado CVSS:4.0/... ou CVSS:3.1/...", is_warning=True))

    # Validar integridade referencial deriva_de
    for item in achados:
        if isinstance(item, dict):
            deriva = item.get("deriva_de")
            if deriva and str(deriva) not in known_ids:
                errors.append(ValidationError(str(item.get("id")), "deriva_de", f"deriva_de referencia ID inexistente: '{deriva}'"))

    # Validar sincronia com resumo
    resumo = data.get("resumo")
    if not isinstance(resumo, dict):
        errors.append(ValidationError("resumo", "resumo", "Bloco 'resumo' ausente ou inválido"))
    else:
        for k in ["total", "critico", "alto", "medio", "baixo", "info"]:
            declared = resumo.get(k, 0)
            actual = actual_counts.get(k, 0)
            if declared != actual:
                errors.append(ValidationError("resumo", k, f"Contagem divergente no resumo para '{k}': declarado={declared}, real={actual}"))

    return errors, data


def execute_validate(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if target.is_dir():
        target = target / "achados.yaml"

    print(colorize(f"==> Validando: {target}", Colors.CYAN + Colors.BOLD))
    errors, data = validate_audit_file(target)

    fatal_errors = [e for e in errors if not e.is_warning]
    warnings = [e for e in errors if e.is_warning]

    if warnings:
        print(colorize(f"\n[AVISOS] ({len(warnings)}):", Colors.YELLOW + Colors.BOLD))
        for w in warnings:
            print(f"  - [{w.finding_id}] {w.field}: {w.message}")

    if fatal_errors:
        print(colorize(f"\n[FALHAS DE VALIDAÇÃO] ({len(fatal_errors)}):", Colors.RED + Colors.BOLD))
        for err in fatal_errors:
            print(f"  - [{err.finding_id}] {err.field}: {err.message}")
        print(colorize(f"\nResultado: REPROVADO ({len(fatal_errors)} erro(s)).", Colors.RED + Colors.BOLD))
        return 1

    total = len(data.get("achados", []))
    print(colorize(f"\n[OK] Validação aprovada! ({total} achados verificados sem erros de schema)", Colors.GREEN + Colors.BOLD))
    return 0


# ==============================================================================
# Geração de Relatório (Report Compiler)
# ==============================================================================

def generate_markdown_report(data: Dict[str, Any]) -> str:
    meta = data.get("meta", {})
    resumo = data.get("resumo", {})
    achados = data.get("achados", [])

    produto = meta.get("produto", "Produto")
    dt_inicio = meta.get("data_inicio", date.today().isoformat())
    dt_fim = meta.get("data_fim") or date.today().isoformat()
    auditor = meta.get("auditor", "Security Audit Framework")
    escopo = meta.get("escopo", "Escopo da auditoria")

    # Ordenar achados por severidade
    sorted_achados = sorted(
        achados,
        key=lambda x: (SEVERITY_ORDER.get(str(x.get("severidade", "")).lower(), 99), str(x.get("id", "")))
    )

    lines: List[str] = [
        f"# Relatório de Auditoria de Segurança — {produto}",
        "",
        "> **CONFIDENCIAL — uso restrito.** Este documento descreve a avaliação de segurança,",
        f"> conformidade e vulnerabilidades do sistema {produto}.",
        "",
        "---",
        "",
        "## Informações gerais",
        "",
        "| Campo | Valor |",
        "|-------|-------|",
        f"| **Produto** | {produto} |",
        f"| **Período** | {dt_inicio} a {dt_fim} |",
        f"| **Auditor** | {auditor} |",
        f"| **Escopo** | {escopo} |",
        f"| **Metodologia** | Security Audit Framework v{FRAMEWORK_VERSION} (4 pilares) |",
        f"| **Data do Laudo** | {date.today().isoformat()} |",
        "",
        "---",
        "",
        "## Resumo Executivo e Estatísticas",
        "",
        "| Severidade | Quantidade |",
        "|------------|------------|",
        f"| **Crítico** | {resumo.get('critico', 0)} |",
        f"| **Alto** | {resumo.get('alto', 0)} |",
        f"| **Médio** | {resumo.get('medio', 0)} |",
        f"| **Baixo** | {resumo.get('baixo', 0)} |",
        f"| **Info** | {resumo.get('info', 0)} |",
        f"| **Total** | **{resumo.get('total', len(achados))}** |",
        "",
        "### Matriz de Risco",
        "",
        "| ↓ Severidade / Status → | Confirmado | Rascunho | Corrigido | Falso Positivo |",
        "|---|---|---|---|---|",
    ]

    for s in ["critico", "alto", "medio", "baixo", "info"]:
        s_items = [a for a in sorted_achados if str(a.get("severidade", "")).lower() == s]
        conf = sum(1 for a in s_items if str(a.get("status", "")).lower() == "confirmado")
        rasc = sum(1 for a in s_items if str(a.get("status", "")).lower() == "rascunho")
        corr = sum(1 for a in s_items if str(a.get("status", "")).lower() == "corrigido")
        fp = sum(1 for a in s_items if str(a.get("status", "")).lower() == "falso_positivo")
        lines.append(f"| **{s.capitalize()}** | {conf} | {rasc} | {corr} | {fp} |")

    lines.extend([
        "",
        "---",
        "",
        "## Detalhamento Técnico dos Achados",
        "",
    ])

    for a in sorted_achados:
        aid = a.get("id", "AUD-XXX")
        title = a.get("titulo", "Achado")
        sev = str(a.get("severidade", "info")).upper()
        status = str(a.get("status", "rascunho")).upper()
        cvss = a.get("cvss", "N/A")
        owasp = a.get("owasp", "N/A")
        cwe = a.get("cwe", "N/A")
        loc = a.get("localizacao", "N/A")
        desc = a.get("descricao", "").strip()
        poc = a.get("poc", "").strip()
        impact = a.get("impacto", "").strip()
        remed = a.get("remediacao", "").strip()
        reteste = str(a.get("reteste", "pendente")).upper()

        lines.extend([
            f"### [{aid}] {title}",
            "",
            f"- **Severidade:** `{sev}` | **Status:** `{status}` | **Reteste:** `{reteste}`",
            f"- **CVSS:** `{cvss}`",
            f"- **OWASP:** {owasp} | **CWE:** `{cwe}`",
            f"- **Localização:** `{loc}`",
            "",
            "#### Descrição e Causa Raiz",
            desc or "_Sem descrição detalhada._",
            "",
            "#### Prova de Conceito (PoC)",
            "```bash",
            poc or "# Sem PoC cadastrada",
            "```",
            "",
            "#### Impacto",
            impact or "_Impacto não especificado._",
            "",
            "#### Remediação Recomendada",
            remed or "_Remediação não especificada._",
            "",
            "---",
            "",
        ])

    lines.extend([
        "## Roadmap de Remediação por Sprint",
        "",
        "### Sprint 1 — Emergencial (Críticos)",
    ])
    criticos = [a for a in sorted_achados if str(a.get("severidade", "")).lower() == "critico" and str(a.get("status", "")).lower() != "falso_positivo"]
    if criticos:
        for a in criticos:
            lines.append(f"- [ ] **{a.get('id')}**: {a.get('titulo')} (`{a.get('localizacao')}`)")
    else:
        lines.append("_Nenhum achado crítico pendente._")

    lines.extend([
        "",
        "### Sprint 2 — Alta Prioridade (Altos)",
    ])
    altos = [a for a in sorted_achados if str(a.get("severidade", "")).lower() == "alto" and str(a.get("status", "")).lower() != "falso_positivo"]
    if altos:
        for a in altos:
            lines.append(f"- [ ] **{a.get('id')}**: {a.get('titulo')} (`{a.get('localizacao')}`)")
    else:
        lines.append("_Nenhum achado de alta severidade pendente._")

    lines.extend([
        "",
        "### Sprint 3 — Qualidade e Hardening (Médios e Baixos)",
    ])
    medios = [a for a in sorted_achados if str(a.get("severidade", "")).lower() in ["medio", "baixo"] and str(a.get("status", "")).lower() != "falso_positivo"]
    if medios:
        for a in medios:
            lines.append(f"- [ ] **{a.get('id')}**: {a.get('titulo')} (`{a.get('localizacao')}`)")
    else:
        lines.append("_Nenhum achado médio/baixo pendente._")

    lines.extend([
        "",
        "---",
        f"_Relatório gerado automaticamente por audit_tool.py — Security Audit Framework v{FRAMEWORK_VERSION}_",
        "",
    ])

    return "\n".join(lines)


def execute_report(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if target.is_dir():
        achados_file = target / "achados.yaml"
        output_file = target / "relatorio-final.md"
    else:
        achados_file = target
        output_file = achados_file.parent / "relatorio-final.md"

    if args.output:
        output_file = Path(args.output).resolve()

    print(colorize(f"==> Compilando laudo a partir de: {achados_file}", Colors.CYAN + Colors.BOLD))
    errors, data = validate_audit_file(achados_file)
    fatal_errors = [e for e in errors if not e.is_warning]
    if fatal_errors:
        print(colorize(f"AVISO: {len(fatal_errors)} erros de validação detectados. O laudo será gerado, mas revise os erros com 'audit_tool.py validate'.", Colors.YELLOW))

    report_md = generate_markdown_report(data)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(colorize(f"[OK] Relatório gerado com sucesso: {output_file}", Colors.GREEN + Colors.BOLD))
    return 0


# ==============================================================================
# Estatísticas Rápidas (CLI Stats)
# ==============================================================================

def execute_stats(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if target.is_dir():
        target = target / "achados.yaml"

    if not target.is_file():
        print(f"ERRO: arquivo não encontrado: {target}", file=sys.stderr)
        return 1

    with open(target, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    meta = data.get("meta", {})
    resumo = data.get("resumo", {})
    achados = data.get("achados", [])

    print(colorize(f"\n--- Auditoria: {meta.get('produto', 'N/A')} ({meta.get('data_inicio', '')}) ---", Colors.BOLD))
    print(f"Total: {resumo.get('total', len(achados))} | "
          f"{colorize('Crítico: ' + str(resumo.get('critico', 0)), Colors.RED + Colors.BOLD)} | "
          f"{colorize('Alto: ' + str(resumo.get('alto', 0)), Colors.RED)} | "
          f"{colorize('Médio: ' + str(resumo.get('medio', 0)), Colors.YELLOW)} | "
          f"{colorize('Baixo: ' + str(resumo.get('baixo', 0)), Colors.BLUE)}")

    print("\n" + "=" * 95)
    print(f"{'ID':<9} {'SEV':<8} {'STATUS':<11} {'RETESTE':<10} {'TÍTULO'}")
    print("=" * 95)
    for a in achados:
        aid = a.get("id", "")
        sev = str(a.get("severidade", "")).lower()
        st = str(a.get("status", ""))
        ret = str(a.get("reteste", ""))
        title = a.get("titulo", "")[:50]
        sev_str = colorize(f"{sev:<8}", severity_color(sev))
        print(f"{aid:<9} {sev_str} {st:<11} {ret:<10} {title}")
    print("=" * 95 + "\n")
    return 0


# ==============================================================================
# Seleção Eficiente de Prompts para Agentes de IA (Token Saver)
# ==============================================================================

def execute_select(args: argparse.Namespace) -> int:
    """Carrega o catálogo de prompts e filtra os mais relevantes para o stack."""
    root_dir = Path(__file__).resolve().parent.parent
    catalog_file = root_dir / "catalog" / "prompts.json"

    if not catalog_file.is_file():
        print(f"ERRO: catálogo de prompts não encontrado em {catalog_file}", file=sys.stderr)
        return 1

    with open(catalog_file, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    stack_terms = [t.strip().lower() for t in args.stack.split(",") if t.strip()]

    print(colorize(f"==> Selecionando prompts para stack: {', '.join(stack_terms)}", Colors.CYAN + Colors.BOLD))

    selected = []
    for item in catalog:
        triggers = [tr.lower() for tr in item.get("triggers", [])]
        # Prompts obrigatórios de core
        is_core = item.get("pilar") in ["analisar", "descobrir"] and item.get("categoria") in ["auth", "injection", "recon", "surface"]
        matches_stack = any(st in triggers for st in stack_terms) or not triggers

        if is_core or matches_stack:
            selected.append(item)

    print(f"Prompts selecionados: {len(selected)} de {len(catalog)} disponíveis\n")
    for p in selected:
        print(f"• [{colorize(p.get('pilar', '').upper(), Colors.BOLD)}] {p.get('title')} ({p.get('path')})")
        if args.verbose:
            print(f"  OWASP: {p.get('owasp', 'N/A')} | Triggers: {', '.join(p.get('triggers', []))}")
            print(f"  Intenção: {p.get('intencao', '')}\n")

    return 0


# ==============================================================================
# CLI Entrypoint
# ==============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="audit_tool.py — Automação do Security Audit Framework v1.4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando: ingest
    p_ingest = subparsers.add_parser("ingest", help="Ingerir raw-scans/*.json em achados.yaml")
    p_ingest.add_argument("audit_dir", help="Caminho da pasta da auditoria (ex: auditorias/produto-data)")
    p_ingest.add_argument("--min-severity", default="medio", choices=["critico", "alto", "medio", "baixo", "info"], help="Severidade mínima para criar rascunho (default: medio)")
    p_ingest.add_argument("--include-vendor", action="store_true", help="Incluir diretórios vendor e node_modules (default: false)")
    p_ingest.add_argument("--dry-run", action="store_true", help="Simular sem alterar achados.yaml")

    # Subcomando: validate
    p_validate = subparsers.add_parser("validate", help="Validar schema e consistência do achados.yaml")
    p_validate.add_argument("target", help="Caminho do achados.yaml ou da pasta da auditoria")

    # Subcomando: report
    p_report = subparsers.add_parser("report", help="Gerar relatorio-final.md a partir de achados.yaml")
    p_report.add_argument("target", help="Caminho do achados.yaml ou da pasta da auditoria")
    p_report.add_argument("-o", "--output", help="Caminho de saída customizado do arquivo Markdown")

    # Subcomando: stats
    p_stats = subparsers.add_parser("stats", help="Exibir resumo tabular dos achados no terminal")
    p_stats.add_argument("target", help="Caminho do achados.yaml ou da pasta da auditoria")

    # Subcomando: select
    p_select = subparsers.add_parser("select", help="Selecionar prompts ideais por stack para economizar tokens")
    p_select.add_argument("--stack", required=True, help="Lista separada por vírgula (ex: laravel,vue,ai,docker,mcp)")
    p_select.add_argument("-v", "--verbose", action="store_true", help="Exibir detalhes do prompt")

    args = parser.parse_args()

    if args.command == "ingest":
        return execute_ingest(args)
    elif args.command == "validate":
        return execute_validate(args)
    elif args.command == "report":
        return execute_report(args)
    elif args.command == "stats":
        return execute_stats(args)
    elif args.command == "select":
        return execute_select(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
