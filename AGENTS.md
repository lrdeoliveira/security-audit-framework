# AGENTS.md — Instruções para Agentes Autônomos (Antigravity / Claude Code / Cursor / Codex)

Este repositório é o **Security Audit Framework v1.4**, uma metodologia assistida por automação e orientada a prompts para auditorias de segurança web, cloud, infra e sistemas de IA/LLM/MCP.

Ao atuar como agente neste repositório ou utilizando este framework para auditar um alvo, siga estritamente estas diretrizes.

---

## 1. Regra Zero: Autorização e Ética
- **NUNCA** execute testes ativos, scans destrutivos ou ataques contra alvos sem autorização explícita por escrito do proprietário.
- Toda exploração dinâmica (Pilar 3) deve ser **não-destrutiva**: demonstre explorabilidade sem derrubar o serviço, sem exfiltrar dados reais de terceiros e sem corromper o banco.

---

## 2. Eficiência de Contexto e Tokens (Regra de Ouro)
- **NÃO leia todos os 40 arquivos `.md` das pastas `01-descobrir/`, `02-analisar/`, etc.** Isso consome ~25.000 tokens desnecessariamente.
- **Utilize o catálogo centralizado:**
  - `catalog/prompts.json` (ou `catalog/prompts.yaml`): contém todos os prompts indexados com seus triggers, OWASP, CWE e instruções de teste.
  - Ou execute via terminal:
    ```bash
    python3 scripts/audit_tool.py select --stack <tecnologias>
    # Exemplo: python3 scripts/audit_tool.py select --stack laravel,vue,ai
    ```
- Leia somente os prompts pontuais recomendados para o escopo e stack do alvo.

---

## 3. Fluxo de Execução Recomendado

```
1. Bootstrap Scan (Paralelo)  ──>  2. Ingestão Automática  ──>  3. Triagem & Validação  ──>  4. Compilação do Laudo
   (bootstrap-scan.sh)             (audit_tool.py ingest)        (audit_tool.py validate)      (audit_tool.py report)
```

### Passo 1: Executar o Bootstrap Scan
Rode os scanners base em paralelo contra o repositório alvo:
```bash
./00-orquestrador/bootstrap-scan.sh --parallel /caminho/do/alvo nome-do-produto
# Ou via Makefile:
make scan REPO=/caminho/do/alvo PROD=nome-do-produto
```
_Saídas geradas em: `auditorias/{produto}-{data}/raw-scans/` e `pre-scan.md`._

### Passo 2: Ingerir os Achados
Transforme automaticamente as saídas dos scanners em rascunhos estruturados em `achados.yaml`:
```bash
python3 scripts/audit_tool.py ingest auditorias/{produto}-{data}
# Ou via Makefile:
make ingest AUDIT=auditorias/{produto}-{data}
```

### Passo 3: Triagem, Análise Profunda e DAST
- Abra `auditorias/{produto}-{data}/achados.yaml`.
- Para cada finding:
  - Se for falso positivo: altere `status: falso_positivo`.
  - Se confirmado: altere `status: confirmado`, preencha o campo `poc` e `remediacao`.
- Para vulnerabilidades de lógica de negócio, auth bypass, IDOR ou testes de IA (OWASP LLM Top 10 2025): consulte os prompts recomendados e crie novos cards `AUD-NNN`.

### Passo 4: Validar o Arquivo de Achados
Sempre rode o validador antes de concluir para garantir conformidade de schema e integridade referencial:
```bash
python3 scripts/audit_tool.py validate auditorias/{produto}-{data}
# Ou via Makefile:
make validate AUDIT=auditorias/{produto}-{data}
```

### Passo 5: Compilar o Relatório Final
Gere o laudo executivo e técnico estruturado em Markdown:
```bash
python3 scripts/audit_tool.py report auditorias/{produto}-{data}
# Ou via Makefile:
make report AUDIT=auditorias/{produto}-{data}
```

---

## 4. Invariantes do Schema `achados.yaml`
1. `id`: Formato `AUD-NNN` sequencial e único.
2. `severidade`: Exclusivamente `critico`, `alto`, `medio`, `baixo` ou `info`.
3. `status`: Exclusivamente `rascunho`, `confirmado`, `falso_positivo` ou `corrigido`.
4. `reteste`: Exclusivamente `pendente`, `aprovado` ou `reprovado`.
5. `cvss`: Padrão `CVSS:4.0/...` (ou `CVSS:3.1/...`).
6. `deriva_de`: Se preenchido, deve apontar para um `id` existente no mesmo arquivo.
7. `resumo`: Os totais declarados (`total`, `critico`, `alto`, `medio`, `baixo`, `info`) devem bater com o somatório exato da lista `achados`.

---

## 5. Ferramental Disponível
- `00-orquestrador/bootstrap-scan.sh`: Ingestão paralela com timeouts e flags de filtro.
- `scripts/audit_tool.py`: CLI de automação (subcomandos `ingest`, `validate`, `report`, `stats`, `select`).
- `catalog/prompts.json`: Catálogo estruturado de prompts.
- `Makefile`: Automação rápida de tarefas frequentes.
