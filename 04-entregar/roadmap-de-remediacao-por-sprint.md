# Roadmap de remediação por sprint

**Pilar:** entregar
**Fase:** 5 / pós-auditoria
**Categoria:** reporting
**OWASP:** —
**Ferramentas sugeridas:** —
**Intenção:** Priorizar e distribuir correções de segurança em sprints de acordo com risco e esforço.

## Como usar
Forneça a lista de achados abertos com severidade. Inclua contexto sobre a capacidade do time (número de devs, duração do sprint) se disponível.

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
(4) Para cada achado: estimativa de esforço em horas, dependências técnicas, critério de verificação e responsável sugerido (o relatório final tem coluna "Responsável");
(5) Gates de reteste: pontos no roadmap onde um reteste parcial ou completo é recomendado;
(6) Métricas de progresso: como medir redução de risco ao longo das sprints;
(7) SLA de remediação por severidade: prazo-alvo de correção por criticidade (ex: Crítico ≤7d, Alto ≤30d, Médio ≤90d, Baixo/Info best-effort), usado para priorizar as sprints;
(8) Critério de aceite de risco (risk acceptance): para achado que o negócio decide não corrigir, registrar dono, justificativa, prazo de reavaliação e assinatura do responsável.
```

## Saída esperada
Roadmap de remediação em sprints com estimativas, dependências, gates de reteste e métricas de progresso.

## Onde usar no fluxo
Fase 5 - Relatório / Planejamento de remediação. Entregue junto com o relatório para o time de desenvolvimento. Consulte `AUDITORIA.md` para o checklist completo.
