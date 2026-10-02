---
name: security-audit
description: Conduz uma auditoria de segurança completa (pentest assistido) de um repositório, aplicação web, infra ou sistema com IA/LLM/MCP, seguindo o Security Audit Framework v1.4. Automatiza ingestão via scanners concorrentes, triagem de findings, validação de schema e geração de laudo executivo/técnico.
---

# Security Audit — Condutor do Framework v1.4

Esta skill executa o **Security Audit Framework** de ponta a ponta com alta eficiência de execução e de tokens.

## 0. Pré-requisitos (faça SEMPRE antes de começar)

1. **Autorização.** Confirme com o usuário que ele tem permissão para auditar o alvo (sistema próprio, engajamento com autorização escrita, CTF, ou pesquisa autorizada). Sem autorização clara, **pare e pergunte**.
2. **Localize o framework.** Encontre o `AUDITORIA.md` (ponto de entrada) e os scripts em `scripts/`.
3. **Defina o escopo.** URLs, repositórios, ambientes (dev/staging/prod), e o que está fora do escopo.
4. **Crie a auditoria.** A pasta de trabalho será `auditorias/{produto}-{data}/`.

## 1. Fluxo Otimizado v1.4

```
bootstrap-scan (paralelo) → ingest (achados.yaml) → validar/DAST → validate (schema) → report
                                                            ↑________ reteste __________|
```

### Passo 1: Ingestão Automatizada Concorrente
Execute o scan paralelo base para mapear vulnerabilidades estáticas, segredos e dependências:
```bash
./00-orquestrador/bootstrap-scan.sh --parallel /caminho/do/alvo <produto>
# Ou via Makefile:
make scan REPO=/caminho/do/alvo PROD=<produto>
```

### Passo 2: Ingestão Estruturada dos Achados
Importe automaticamente os resultados dos scanners para o `achados.yaml` com severidades, CWE e OWASP mapeados:
```bash
python3 scripts/audit_tool.py ingest auditorias/{produto}-{data}
# Ou via Makefile:
make ingest AUDIT=auditorias/{produto}-{data}
```

### Passo 3: Análise e Validação Dirigida
Para economizar tokens, consulte os prompts relevantes ao stack sem abrir dezenas de arquivos:
```bash
python3 scripts/audit_tool.py select --stack <tecnologias>
# Exemplo: python3 scripts/audit_tool.py select --stack laravel,vue,ai,docker
```
- Triague os achados em `achados.yaml`: marque falsos positivos como `status: falso_positivo`, e confirme falhas reais como `status: confirmado` adicionando PoC.
- Para testes dinâmicos (DAST, lógica de negócio, SSRF, IDOR, AI Red Teaming): exercite os vetores indicados pelos prompts selecionados.

### Passo 4: Validação do Schema e Coerência
Valide o arquivo de achados antes da entrega:
```bash
python3 scripts/audit_tool.py validate auditorias/{produto}-{data}
# Ou via Makefile:
make validate AUDIT=auditorias/{produto}-{data}
```

### Passo 5: Compilação do Laudo Final
Gere o laudo em Markdown (`relatorio-final.md`) com sumário executivo, matriz de risco, detalhamento técnico e roadmap:
```bash
python3 scripts/audit_tool.py report auditorias/{produto}-{data}
# Ou via Makefile:
make report AUDIT=auditorias/{produto}-{data}
```

## 2. Boas Práticas
- **Severidade honesta:** Use a escala de risco do `AUDITORIA.md` (CVSS 4.0).
- **Sem dano:** Testes em produção devem ser estritamente não-destrutivos.
- **Loop de reteste:** Atualize o campo `reteste: aprovado | reprovado` após correções.
