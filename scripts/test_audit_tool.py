#!/usr/bin/env python3
"""
test_audit_tool.py — Suíte de testes unitários e de integração para audit_tool.py
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_tool import (
    Finding,
    generate_markdown_report,
    ingest_raw_scans,
    map_checkov_to_finding,
    map_gitleaks_to_finding,
    map_semgrep_to_finding,
    map_trivy_vuln_to_finding,
    map_trufflehog_to_finding,
    validate_audit_file,
)


class TestAuditTool(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_audit_"))

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_map_semgrep(self):
        raw = {
            "check_id": "python.flask.security.audit.render-template-string.render-template-string",
            "path": "app.py",
            "start": {"line": 42},
            "extra": {
                "severity": "ERROR",
                "message": "Template injection detected",
                "metadata": {
                    "cwe": ["CWE-1336: Improper Neutralization of Special Elements used in a Template Engine"],
                    "owasp": ["A03:2021 - Injection"],
                },
            },
        }
        f = map_semgrep_to_finding(raw, next_id=1)
        self.assertEqual(f.id, "AUD-001")
        self.assertEqual(f.severidade, "alto")
        self.assertEqual(f.cwe, "CWE-1336")
        self.assertEqual(f.owasp, "A03:2021 - Injection")
        self.assertEqual(f.localizacao, "app.py:42")
        self.assertEqual(f.prompt_origem, "02-analisar/revisao-de-injection-e-execucao-arbitraria.md")

    def test_map_gitleaks(self):
        raw = {
            "RuleID": "aws-access-token",
            "File": ".env.sample",
            "StartLine": 10,
            "Commit": "abc123456789",
            "Secret": "AKIAIOSFODNN7EXAMPLE",
        }
        f = map_gitleaks_to_finding(raw, next_id=2)
        self.assertEqual(f.id, "AUD-002")
        self.assertEqual(f.severidade, "alto")
        self.assertEqual(f.cwe, "CWE-798")
        self.assertIn("commit abc12345", f.localizacao)

    def test_map_trufflehog_verified(self):
        raw = {
            "DetectorName": "Slack",
            "Verified": True,
            "SourceMetadata": {
                "Data": {
                    "Filesystem": {"file": "config/slack.py", "line": 15}
                }
            },
        }
        f = map_trufflehog_to_finding(raw, next_id=3)
        self.assertEqual(f.id, "AUD-003")
        self.assertEqual(f.severidade, "critico")
        self.assertIn("VERIFICADO", f.titulo)

    def test_map_trivy(self):
        vuln = {
            "VulnerabilityID": "CVE-2026-12345",
            "PkgName": "urllib3",
            "InstalledVersion": "1.26.5",
            "FixedVersion": "1.26.18",
            "Severity": "HIGH",
            "Description": "Header injection vulnerability",
            "CweIDs": ["CWE-113"],
        }
        f = map_trivy_vuln_to_finding(vuln, "requirements.txt", next_id=4)
        self.assertEqual(f.id, "AUD-004")
        self.assertEqual(f.severidade, "alto")
        self.assertEqual(f.cwe, "CWE-113")
        self.assertIn("urllib3@1.26.5", f.localizacao)

    def test_map_checkov(self):
        check = {
            "check_id": "CKV_DOCKER_2",
            "check_name": "Ensure that HEALTHCHECK instructions have been added to container images",
            "file_path": "Dockerfile",
            "file_line_range": [1, 20],
            "guideline": "https://docs.bridgecrew.io/docs/ensure-that-healthcheck-instructions-have-been-added-to-container-images",
        }
        f = map_checkov_to_finding(check, next_id=5)
        self.assertEqual(f.id, "AUD-005")
        self.assertEqual(f.severidade, "medio")
        self.assertEqual(f.cwe, "CWE-16")

    def test_ingest_and_validation_cycle(self):
        raw_dir = self.test_dir / "raw-scans"
        raw_dir.mkdir(parents=True)

        # Criar fixture de semgrep
        semgrep_sample = {
            "results": [
                {
                    "check_id": "python.jwt.hardcoded-jwt-secret",
                    "path": "auth.py",
                    "start": {"line": 12},
                    "extra": {
                        "severity": "ERROR",
                        "message": "Hardcoded JWT secret",
                        "metadata": {"cwe": ["CWE-798"], "owasp": ["A02:2021"]},
                    },
                }
            ]
        }
        with open(raw_dir / "semgrep.json", "w", encoding="utf-8") as f:
            json.dump(semgrep_sample, f)

        findings = ingest_raw_scans(self.test_dir, min_severity="medio")
        self.assertEqual(len(findings), 1)

        # Salvar achados.yaml
        achados_file = self.test_dir / "achados.yaml"
        payload = {
            "meta": {
                "produto": "SistemaTeste",
                "data_inicio": "2026-10-02",
                "auditor": "Tester",
                "escopo": "Teste",
            },
            "resumo": {
                "total": 1,
                "critico": 0,
                "alto": 1,
                "medio": 0,
                "baixo": 0,
                "info": 0,
            },
            "achados": [findings[0].to_dict()],
        }
        with open(achados_file, "w", encoding="utf-8") as f:
            yaml.dump(payload, f)

        errors, data = validate_audit_file(achados_file)
        fatal = [e for e in errors if not e.is_warning]
        self.assertEqual(len(fatal), 0, f"Erros inesperados: {fatal}")

        # Gerar relatório
        report_md = generate_markdown_report(data)
        self.assertIn("# Relatório de Auditoria de Segurança — SistemaTeste", report_md)
        self.assertIn("AUD-001", report_md)
        self.assertIn("auth.py:12", report_md)

    def test_validation_detects_errors(self):
        achados_file = self.test_dir / "invalid.yaml"
        invalid_payload = {
            "meta": {"produto": "App"},  # falta data_inicio
            "resumo": {"total": 5, "critico": 0, "alto": 0, "medio": 0, "baixo": 0, "info": 0},  # contagem errada
            "achados": [
                {
                    "id": "INVALID-ID",
                    "titulo": "Titulo",
                    "severidade": "super_grave",  # severidade inválida
                    "pilar": "analisar",
                    "status": "ativo",  # status inválido
                    "reteste": "talvez",  # reteste inválido
                    "deriva_de": "AUD-999",  # id inexistente
                }
            ],
        }
        with open(achados_file, "w", encoding="utf-8") as f:
            yaml.dump(invalid_payload, f)

        errors, _ = validate_audit_file(achados_file)
        err_fields = [e.field for e in errors]
        self.assertIn("data_inicio", err_fields)
        self.assertIn("id", err_fields)
        self.assertIn("severidade", err_fields)
        self.assertIn("status", err_fields)
        self.assertIn("reteste", err_fields)
        self.assertIn("deriva_de", err_fields)
        self.assertIn("total", err_fields)


if __name__ == "__main__":
    unittest.main()
