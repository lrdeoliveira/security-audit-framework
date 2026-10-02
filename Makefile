# ==============================================================================
# Security Audit Framework v1.4 — Makefile
# Automação de varreduras, ingestão, validação e compilação de laudos
# ==============================================================================

SHELL := /bin/bash
PYTHON ?= python3

.PHONY: help scan scan-fast scan-auto ingest validate report stats select catalog test clean

help:
	@echo "======================================================================"
	@echo "  Security Audit Framework v1.4 — Comandos Rápidos"
	@echo "======================================================================"
	@echo "  make scan REPO=<dir> PROD=<nome>       Executa bootstrap-scan paralelo"
	@echo "  make scan-fast REPO=<dir> PROD=<nome>  Executa scan rápido (SAST + segredos)"
	@echo "  make scan-auto REPO=<dir> PROD=<nome>  Scan paralelo + auto-ingest no achados.yaml"
	@echo "  make ingest AUDIT=<dir>                Ingere raw-scans/*.json em achados.yaml"
	@echo "  make validate AUDIT=<dir>              Valida regras e schema do achados.yaml"
	@echo "  make report AUDIT=<dir>                Compila achados.yaml em relatorio-final.md"
	@echo "  make stats AUDIT=<dir>                 Exibe tabela de achados no terminal"
	@echo "  make select STACK=<lista>              Filtra prompts recomendados por stack"
	@echo "  make catalog                           Regenera o catálogo de prompts (JSON/YAML)"
	@echo "  make test                              Roda suíte de testes do framework"
	@echo "  make clean                             Remove artefatos temporários de teste"
	@echo "======================================================================"

check-args:
	@if [ -z "$(REPO)" ] || [ -z "$(PROD)" ]; then \
		echo "ERRO: Informe REPO e PROD. Exemplo: make scan REPO=~/proj PROD=minha-app"; \
		exit 1; \
	fi

check-audit:
	@if [ -z "$(AUDIT)" ]; then \
		echo "ERRO: Informe AUDIT. Exemplo: make validate AUDIT=auditorias/minha-app-2026-10-02"; \
		exit 1; \
	fi

scan: check-args
	@./00-orquestrador/bootstrap-scan.sh --parallel "$(REPO)" "$(PROD)"

scan-fast: check-args
	@./00-orquestrador/bootstrap-scan.sh --fast "$(REPO)" "$(PROD)"

scan-auto: check-args
	@./00-orquestrador/bootstrap-scan.sh --parallel --auto-ingest "$(REPO)" "$(PROD)"

ingest: check-audit
	@$(PYTHON) scripts/audit_tool.py ingest "$(AUDIT)"

validate: check-audit
	@$(PYTHON) scripts/audit_tool.py validate "$(AUDIT)"

report: check-audit
	@$(PYTHON) scripts/audit_tool.py report "$(AUDIT)"

stats: check-audit
	@$(PYTHON) scripts/audit_tool.py stats "$(AUDIT)"

select:
	@if [ -z "$(STACK)" ]; then \
		echo "ERRO: Informe STACK. Exemplo: make select STACK=laravel,vue,ia"; \
		exit 1; \
	fi
	@$(PYTHON) scripts/audit_tool.py select --stack "$(STACK)"

catalog:
	@$(PYTHON) scripts/build_catalog.py

test:
	@$(PYTHON) -m unittest scripts/test_audit_tool.py

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf .pytest_cache .coverage 2>/dev/null || true
