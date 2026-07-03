# Relatório de Auditoria de Segurança

> **CONFIDENCIAL — uso restrito.** Este documento descreve vulnerabilidades de um
> sistema em produção. Distribua apenas às partes autorizadas.
>
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
| **Base de autorização** | {{CONTRATO_OU_AUTORIZACAO}} — abordagem black / grey / white-box |
| **Classificação** | CONFIDENCIAL |
| **Metodologia** | Security Audit Framework v1.3 — 4 pilares (Descobrir, Analisar, Validar, Entregar) |
| **Versão do documento** | 1.0 |

---

## Disclaimer e limitações

- Esta auditoria é um retrato **point-in-time**: reflete o estado do alvo durante a janela de teste ({{DATA_INICIO}}–{{DATA_FIM}}). Mudanças posteriores não estão cobertas.
- Os testes foram executados **sob autorização** ({{CONTRATO_OU_AUTORIZACAO}}) e limitados ao escopo acima. Itens fora de escopo não foram avaliados.
- A exploração foi conduzida de forma **não-destrutiva**, apenas o necessário para comprovar cada achado. Nenhum dado real foi exfiltrado nem serviço derrubado propositalmente.
- Ausência de achado em uma área **não garante** ausência de vulnerabilidade — nenhuma auditoria é exaustiva.
- Este relatório é **confidencial** e destinado somente às partes autorizadas por {{NOME_DO_PRODUTO}}.

---

## Metodologia

- **Abordagem:** {{black-box | grey-box | white-box}} — acesso a {{código-fonte / credenciais de teste / apenas superfície pública}}.
- **Padrões de referência:** OWASP Top 10 (2021/2025), OWASP ASVS 5.0, OWASP WSTG, OWASP LLM Top 10 (2025) para componentes de IA, PTES.
- **Fluxo:** `bootstrap-scan` → Descobrir → Analisar (SAST/config/IaC) → Validar (DAST + Red Team + IA) → Entregar, com loop de reteste.
- **Ferramentas:** Semgrep, Trivy, Gitleaks, TruffleHog, osv-scanner, Checkov, mcp-scan, Burp Suite, e (IA) Garak, Promptfoo, PyRIT.
- **Rules of Engagement:** janela {{JANELA_DE_TESTE}}; DoS/brute-force {{permitido | proibido}}; ambiente {{prod | staging}}.
- **Correlação:** achados estáticos (Pilar 2) só viram `confirmado` quando há explorabilidade demonstrada no Pilar 3 (campo `deriva_de`).

---

## Sumário executivo

> Gerado com o prompt [`sumario-executivo-de-pentest`](../04-entregar/sumario-executivo-de-pentest.md)

### Avaliação geral de risco

**Nível:** {{CRITICO | ALTO | MEDIO | BAIXO}}

{{PARAGRAFO_JUSTIFICATIVA}} — inclua o **risco residual** esperado após a remediação e, se houver, a comparação com a auditoria anterior.

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

### Matriz de risco (probabilidade × impacto)

| ↓ Impacto / Probabilidade → | Baixa | Média | Alta |
|-----------------------------|-------|-------|------|
| **Alto**  | Médio | Alto | Crítico |
| **Médio** | Baixo | Médio | Alto |
| **Baixo** | Info | Baixo | Médio |

> Posicione cada `AUD-XXX` na célula correspondente para visualizar a priorização.

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
| CVSS | {{CVSS}} (CVSS 4.0) |
| OWASP | {{OWASP}} |
| CWE | {{CWE}} |
| Localização | {{LOCALIZACAO}} |
| Instâncias afetadas | {{N_INSTANCIAS}} |
| Status | {{STATUS}} |

**Descrição:** {{DESCRICAO}}

**Prova de conceito:**

```
{{POC}}
```

**Impacto:** {{IMPACTO}}

**Recomendação:** {{REMEDIACAO}}

**Evidências:** `evidencias/AUD-001/`  ·  **Referências:** {{CWE_OWASP_CVE}}

---

## Roadmap de remediação

> Gerado com [`roadmap-de-remediacao-por-sprint`](../04-entregar/roadmap-de-remediacao-por-sprint.md). SLA sugerido: Crítico ≤7d · Alto ≤30d · Médio ≤90d · Baixo/Info best-effort.

### Sprint 1 — Críticos e quick wins

| ID | Achado | Severidade | SLA | Esforço | Responsável | Critério de verificação |
|----|--------|-----------|-----|---------|-------------|------------------------|
| AUD-001 | ... | Alto | ≤30d | 4h | ... | Reteste IDOR com 2 usuários |

### Sprint 2 — Altos e médios

| ID | Achado | Severidade | SLA | Esforço | Responsável | Critério de verificação |
|----|--------|-----------|-----|---------|-------------|------------------------|
| ... | ... | ... | ... | ... | ... | ... |

### Sprint 3+ — Melhorias estruturais

{{MELHORIAS_ESTRUTURAIS}}

### Aceite formal de risco (achados não corrigidos)

| ID | Justificativa do negócio | Dono | Prazo de reavaliação | Aprovado por |
|----|--------------------------|------|----------------------|--------------|
| ... | ... | ... | ... | ... |

---

## Resultados de reteste

> Preencha após a remediação, a partir de [`plano-de-reteste-por-achado`](../04-entregar/plano-de-reteste-por-achado.md).

| ID | Achado | Correção verificada | Reteste | Data |
|----|--------|---------------------|---------|------|
| AUD-001 | ... | sim / não | aprovado / reprovado | {{DATA}} |

---

## Conformidade

> Gerado com [`mapeamento-de-conformidade`](../04-entregar/mapeamento-de-conformidade.md). Preencha só os frameworks aplicáveis ao alvo.

| ID | LGPD/GDPR | SOC 2 | ISO 27001 | ASVS 5.0 | PCI DSS | NIST CSF 2.0 / CIS |
|----|-----------|-------|-----------|----------|---------|--------------------|
| AUD-001 | ... | ... | ... | ... | ... | ... |

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

## Histórico de revisão do documento

| Versão | Data | Autor | Mudança |
|--------|------|-------|---------|
| 1.0 | {{DATA_FIM}} | {{AUDITOR}} | Emissão inicial |

---

## Glossário

- **CVSS 4.0** — padrão de pontuação de severidade de vulnerabilidades.
- **IDOR / BOLA** — acesso a objeto de outro usuário por manipulação de identificador.
- **SAST / DAST** — análise estática (código) / dinâmica (aplicação em execução).
- **PoC** — prova de conceito reproduzível do achado.
- **Prompt injection** — instrução maliciosa que subverte o comportamento de um LLM.

---

## Anexos

- `achados.yaml` — registro completo em formato estruturado
- `evidencias/` — screenshots, requests e logs por achado
- `pre-scan.md` + `raw-scans/` — saídas dos scanners automatizados
