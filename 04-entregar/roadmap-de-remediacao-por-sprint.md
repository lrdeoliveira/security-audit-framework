# Roadmap de remediação por sprint

**Pilar:** entregar
**Fase:** 5 / pós-auditoria
**Categoria:** reporting
**OWASP:** —
**Ferramentas sugeridas:** —
**Intenção:** Priorizar e distribuir correções de segurança em sprints de acordo com risco e esforço.

## Como usar
Forneca a lista de achados abertos com severidade. Inclua contexto sobre a capacidade do time (número de devs, duração do sprint) se disponível.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{NOME_DO_PRODUTO}} | Nome do produto ou sistema |
| {{ACHADOS_ABERTOS}} | Lista de achados abertos com severidade e descrição resumida |
| {{CONTEXTO_DO_TIME}} | Tamanho do time, duração do sprint e capacidade disponível para segurança |

## Prompt
```
Com base nos achados abertos de {{NOME_DO_PRODUTO}}: {{ACHADOS_ABERTOS}}, elabore um roadmap de remediação em sprints para {{CONTEXTO_DO_TIME}} com:

(1) Sprint 1 (críticos e quick wins): achados que combinam alto risco com baixo esforço, independente de arquitetura;
(2) Sprint 2 (altos e médios com dependência): achados que requerem refatoração moderada;
(3) Sprint 3+ (melhorias estruturais): achados que demandam mudanças arquiteturais;
(4) Para cada achado: estimativa de esforço em horas, dependências técnicas e critério de verificação;
(5) Gates de reteste: pontos no roadmap onde um reteste parcial ou completo e recomendado;
(6) Metricas de progresso: como medir redução de risco ao longo das sprints.
```

## Saída esperada
Roadmap de remediação em sprints com estimativas, dependências, gates de reteste e métricas de progresso.

## Onde usar no fluxo
Fase 5 - Relatório / Planejamento de remediação. Entregue junto com o relatório para o time de desenvolvimento. Consulte `AUDITORIA.md` para o checklist completo.
