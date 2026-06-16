# Plano de ataque em 5 fases

**Pilar:** orquestrador
**Fase:** planejamento
**Categoria:** red-team
**OWASP:** —
**Ferramentas sugeridas:** Burp Suite, Semgrep, TruffleHog, Garak, Promptfoo, Katana
**Intenção:** Estruturar uma operação de red team completa para o alvo descrito.

## Como usar

Descreva o alvo com stack, funcionalidades principais e contexto de negócio. O prompt gera um plano de ataque estruturado para usar como roteiro da operação.

## Variáveis


| Variável              | Descrição                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------- |
| {{DESCRICAO_DO_ALVO}} | Stack tecnológico, funcionalidades principais, tipo de dado processado e contexto de negócio do alvo |


## Prompt

```
Você é um red teamer sênior de aplicações web e sistemas de IA. Com base no alvo {{DESCRICAO_DO_ALVO}}, elabore um plano de ataque em 5 fases:

(1) Reconhecimento: fontes de informação, ferramentas de mapping, o que coletar antes de qualquer teste ativo;
(2) Análise estática: quais arquivos de código priorizar, quais ferramentas SAST configurar, ordem de revisão;
(3) Análise dinâmica: fluxos críticos para testar, configuração do proxy, ordem de ataque;
(4) Red teaming de IA (se aplicavel): componentes de LLM a atacar, técnicas e ferramentas;
(5) Relatório: estrutura de entregaveis, nível de detalhe técnico e executivo, timeline.

Para cada fase: objetivos concretos, ferramentas específicas, entradas necessarias e saidas esperadas.
```

## Saída esperada

Plano de ataque em 5 fases com objetivos, ferramentas, entradas e saidas por fase.

## Onde usar no fluxo

Planejamento. Execute antes de iniciar qualquer auditoria para definir escopo e sequência de trabalho. Consulte `AUDITORIA.md` para o checklist completo.