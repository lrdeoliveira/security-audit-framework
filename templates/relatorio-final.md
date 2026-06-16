# Relatório de Auditoria de Segurança

> Copie para `auditorias/{produto}-{YYYY-MM-DD}/relatorio-final.md` e preencha.

---

## Informações gerais

| Campo | Valor |
|-------|-------|
| **Produto** | {{NOME_DO_PRODUTO}} |
| **Período** | {{DATA_INICIO}} a {{DATA_FIM}} |
| **Auditor** | {{AUDITOR}} |
| **Escopo** | {{ESCOPO}} |
| **Ambiente** | staging / produção / código-fonte |
| **Metodologia** | Framework proprietário — 4 pilares (Descobrir, Analisar, Validar, Entregar) |

---

## Sumário executivo

> Gerado com o prompt [`sumario-executivo-de-pentest`](../04-entregar/sumario-executivo-de-pentest.md)

### Avaliação geral de risco

**Nível:** {{CRITICO | ALTO | MEDIO | BAIXO}}

{{PARAGRAFO_JUSTIFICATIVA}}

### Top 3 exposições de negócio

1. {{EXPOSICAO_1}}
2. {{EXPOSICAO_2}}
3. {{EXPOSICAO_3}}

### Controles positivos identificados

- {{CONTROLE_1}}
- {{CONTROLE_2}}

### Quick wins (correção rápida, alto impacto)

- [ ] {{QUICK_WIN_1}}
- [ ] {{QUICK_WIN_2}}
- [ ] {{QUICK_WIN_3}}

---

## Estatísticas

| Severidade | Quantidade |
|------------|------------|
| Crítico | 0 |
| Alto | 0 |
| Médio | 0 |
| Baixo | 0 |
| Info | 0 |
| **Total** | **0** |

---

## Superfície de ataque (Pilar 1 — Descobrir)

> Consolidado a partir dos prompts de reconhecimento

### Stack identificada

{{STACK}}

### Endpoints e rotas críticas

{{ENDPOINTS}}

### Integrações externas

{{INTEGRACOES}}

### Componentes de IA (se aplicável)

{{COMPONENTES_IA}}

---

## Achados detalhados

> Uma seção por achado confirmado. Use [`ficha-tecnica-de-achado`](../04-entregar/ficha-tecnica-de-achado.md) para gerar cada entrada.

### AUD-001 — {{TITULO}}

| Campo | Valor |
|-------|-------|
| Severidade | {{SEVERIDADE}} |
| CVSS | {{CVSS}} |
| OWASP | {{OWASP}} |
| CWE | {{CWE}} |
| Status | {{STATUS}} |

**Descrição:** {{DESCRICAO}}

**Prova de conceito:**

```
{{POC}}
```

**Impacto:** {{IMPACTO}}

**Recomendação:** {{REMEDIACAO}}

---

## Roadmap de remediação

> Gerado com [`roadmap-de-remediacao-por-sprint`](../04-entregar/roadmap-de-remediacao-por-sprint.md)

### Sprint 1 — Críticos e quick wins

| ID | Achado | Esforço | Responsável | Critério de verificação |
|----|--------|---------|-------------|------------------------|
| AUD-001 | ... | 4h | ... | Reteste IDOR com 2 usuários |

### Sprint 2 — Altos e médios

| ID | Achado | Esforço | Responsável | Critério de verificação |
|----|--------|---------|-------------|------------------------|
| ... | ... | ... | ... | ... |

### Sprint 3+ — Melhorias estruturais

{{MELHORIAS_ESTRUTURAIS}}

---

## Cobertura da auditoria

### Executado

- [x] Pilar 1 — Descobrir
- [x] Pilar 2 — Analisar
- [x] Pilar 3 — Validar (DAST)
- [ ] Pilar 3 — Validar (IA) — N/A
- [x] Pilar 4 — Entregar

### Fora de escopo / não testado

- {{ITEM_FORA_DE_ESCOPO}}

---

## Próximos passos

1. {{PROXIMO_PASSO_1}}
2. Reteste parcial após Sprint 1
3. Reteste completo após remediação total

---

## Anexos

- `achados.yaml` — registro completo em formato estruturado
- `evidencias/` — screenshots, requests e logs por achado
