# Mapeamento de conformidade

**Pilar:** entregar
**Fase:** 5
**Categoria:** reporting
**OWASP:** OWASP ASVS / OWASP Top 10
**Ferramentas sugeridas:** —
**Intenção:** Traduzir achados técnicos em controles de frameworks de conformidade (LGPD/GDPR, SOC 2, ISO 27001, OWASP ASVS, PCI DSS, NIST CSF 2.0, CIS Controls v8.1) para audiência de risco e compliance.

## Como usar
Cole o `achados.yaml` consolidado e indique quais frameworks são relevantes para o produto (ex: SaaS B2B brasileiro → LGPD + SOC 2; processa cartão → PCI DSS).

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{ACHADOS}} | Conteúdo do achados.yaml consolidado da auditoria |
| {{FRAMEWORKS_ALVO}} | Frameworks aplicáveis: LGPD, GDPR, SOC 2, ISO 27001, OWASP ASVS, PCI DSS, NIST CSF 2.0, CIS Controls v8.1 |

## Prompt
```
Atue como consultor de GRC (governança, risco e conformidade). Dados os achados {{ACHADOS}} e os frameworks {{FRAMEWORKS_ALVO}}, produza:

(1) Matriz achado → controle: para cada achado, os controles violados em cada framework alvo (ex: LGPD Art. 46 segurança; SOC 2 CC6.1; ISO 27001 A.8.x; OWASP ASVS 5.0 (versão 5.0, mai/2025) na notação `v5.0.0-<cap>.<seção>.<req>`, ex: `v5.0.0-1.2.5`; PCI Req-x; NIST CSF 2.0 função.categoria, ex: PR.AA-01; CIS Controls v8.1 Control x.y);
(2) Visão por framework: quais requisitos têm gap aberto, agrupados, com a contagem de achados por requisito;
(3) Achados com impacto regulatório direto: vazamento de dado pessoal (LGPD/GDPR), ausência de logging (SOC 2 CC7), criptografia (ISO A.8.24), retenção e minimização;
(4) Lacunas de programa (não-achado): controles ausentes que a auditoria técnica não cobre mas o framework exige (gestão de acesso, resposta a incidentes, gestão de fornecedores, DPA);
(5) Prioridade de conformidade: o que bloqueia certificação/atestação vs. o que é melhoria;
(6) Linguagem para o relatório: 1 parágrafo por framework resumindo postura e principais gaps para um leitor de compliance.

Não invente requisitos: marque como "verificar" quando o mapeamento depender de contexto não fornecido.
```

## Saída esperada
Matriz achado→controle por framework, visão consolidada de gaps, lacunas de programa e parágrafos prontos para a seção de conformidade do relatório.

## Onde usar no fluxo
Fase 5 - Relatório. Use após consolidar os achados, antes do sumário executivo. Alimenta a seção de conformidade de `templates/relatorio-final.md`. Consulte `AUDITORIA.md` para o checklist completo.
