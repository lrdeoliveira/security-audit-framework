# Plano de reteste por achado

**Pilar:** entregar
**Fase:** 5
**Categoria:** reporting
**OWASP:** —
**Ferramentas sugeridas:** Script gerado, Burp, CI/CD
**Intenção:** Gerar um procedimento de reteste objetivo e reproduzível por achado corrigido, para validar a remediação sem reabrir a auditoria inteira.

## Como usar
Cole o(s) achado(s) corrigido(s) do `achados.yaml` (status `corrigido`) com a PoC original e a remediação aplicada (commit/PR se houver).

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{ACHADOS_CORRIGIDOS}} | Achados com status corrigido: PoC original, remediação aplicada e localização |

## Prompt
```
Atue como auditor responsável por validação de correção. Para cada achado em {{ACHADOS_CORRIGIDOS}}, produza um plano de reteste com:

(1) Pré-condições: usuários/roles, ambiente e dados necessários para reproduzir;
(2) Passo de reteste positivo: reexecutar a PoC original exatamente — resultado esperado agora é falha da exploração;
(3) Testes de bypass: 2-3 variações da PoC que tentam contornar a correção (encoding diferente, outro endpoint/parâmetro, mesma classe em rota irmã) — para evitar correção pontual demais;
(4) Teste de regressão: confirmar que a correção não quebrou o fluxo legítimo;
(5) Critério de aprovação objetivo: o que define reteste = aprovado vs reprovado;
(6) Automação: quando a classe permitir, o caso para incluir no script de scan (referencie 04-entregar/geracao-de-script-de-scan-automatizado.md);
(7) Atualização de registro: setar reteste=aprovado|reprovado e status=corrigido no achados.yaml, com data.

Saída como checklist acionável por achado (AUD-XXX).
```

## Saída esperada
Checklist de reteste por achado (positivo + bypass + regressão), critério de aprovação e ação de atualização do registro.

## Onde usar no fluxo
Fase 5 / loop de reteste. Use quando a equipe reporta correções. Atualiza o campo `reteste` em `achados.yaml` e fecha o ciclo do fluxo em `AUDITORIA.md`. Consulte `AUDITORIA.md` para o checklist completo.
