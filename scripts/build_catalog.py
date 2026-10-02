#!/usr/bin/env python3
"""
build_catalog.py — Indexador do catálogo de prompts do Security Audit Framework
Gera catalog/prompts.json e catalog/prompts.yaml a partir de todos os arquivos
em 00-orquestrador, 01-descobrir, 02-analisar, 03-validar e 04-entregar.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    yaml = None


def extract_prompt_metadata(file_path: Path, root_dir: Path) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    rel_path = file_path.relative_to(root_dir).as_posix()
    slug = file_path.stem

    # Título (# Title)
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else slug

    # Metadados em negrito
    def get_meta(key: str) -> str:
        m = re.search(rf"\*\*{key}:\*\*\s*(.+)$", content, re.MULTILINE)
        return m.group(1).strip() if m else ""

    pilar = get_meta("Pilar")
    fase = get_meta("Fase")
    categoria = get_meta("Categoria")
    owasp = get_meta("OWASP")
    ferramentas = get_meta("Ferramentas sugeridas")
    intencao = get_meta("Intenção")

    # Extrair bloco do prompt
    prompt_match = re.search(r"## Prompt\s+```(?:markdown)?\s*\n(.*?)\n```", content, re.DOTALL)
    prompt_text = prompt_match.group(1).strip() if prompt_match else ""

    # Inferir triggers / tags para filtros inteligentes
    triggers = set()
    combined_text = f"{rel_path} {title} {categoria} {owasp} {intencao}".lower()

    tag_rules = {
        "ia": ["ia", "llm", "rag", "embedding", "prompt", "guardrails", "system-prompt", "wallet"],
        "mcp": ["mcp", "tool-use", "agency", "server-card"],
        "api": ["api", "endpoint", "rota", "rotas", "idor", "rest"],
        "spa": ["spa", "client-side", "xss", "frontend"],
        "auth": ["auth", "autenticacao", "takeover", "jwt", "sessao", "controle-de-acesso", "idor"],
        "injection": ["injection", "sql", "command", "rce", "template"],
        "ssrf": ["ssrf", "traversal", "path-traversal"],
        "secrets": ["segredo", "secret", "gitleaks", "trufflehog", "credential"],
        "crypto": ["cripto", "cipher", "tls", "hash"],
        "iac": ["iac", "docker", "k8s", "terraform", "cloud"],
        "recon": ["fingerprint", "superficie", "recon", "integracoes", "package-manifest"],
        "redteam": ["red-team", "cadeia", "exploracao"],
        "delivery": ["sumario", "roadmap", "reteste", "conformidade", "ficha-tecnica"],
    }

    for tag, keywords in tag_rules.items():
        if any(kw in combined_text for kw in keywords):
            triggers.add(tag)

    return {
        "id": slug,
        "title": title,
        "path": rel_path,
        "pilar": pilar,
        "fase": fase,
        "categoria": categoria,
        "owasp": owasp,
        "ferramentas": ferramentas,
        "intencao": intencao,
        "triggers": sorted(list(triggers)),
        "prompt": prompt_text,
    }


def main():
    root_dir = Path(__file__).resolve().parent.parent
    catalog_dir = root_dir / "catalog"
    catalog_dir.mkdir(exist_ok=True)

    search_dirs = [
        root_dir / "00-orquestrador",
        root_dir / "01-descobrir",
        root_dir / "02-analisar",
        root_dir / "03-validar",
        root_dir / "04-entregar",
    ]

    all_prompts: List[Dict[str, Any]] = []

    for sdir in search_dirs:
        for md_file in sorted(sdir.glob("**/*.md")):
            if md_file.name in ["bootstrap-scan-automatizado.md"]:
                continue
            meta = extract_prompt_metadata(md_file, root_dir)
            all_prompts.append(meta)

    # Ordenar por caminho
    all_prompts.sort(key=lambda x: x["path"])

    json_path = catalog_dir / "prompts.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_prompts, f, ensure_ascii=False, indent=2)

    print(f"Catálogo JSON gerado com sucesso: {json_path} ({len(all_prompts)} prompts indexados)")

    if yaml:
        yaml_path = catalog_dir / "prompts.yaml"
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(all_prompts, f, sort_keys=False, allow_unicode=True)
        print(f"Catálogo YAML gerado com sucesso: {yaml_path}")


if __name__ == "__main__":
    main()
