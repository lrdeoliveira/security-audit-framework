# Plano de ataque em 5 fases

**Pilar:** orquestrador
**Fase:** planejamento
**Categoria:** red-team
**OWASP:** —
**Ferramentas sugeridas:** Burp Suite, Semgrep, TruffleHog, Garak, Promptfoo, Katana, Trivy, Gitleaks, osv-scanner, Checkov, mcp-scan
**Intenção:** Estruturar uma operação de red team completa para o alvo descrito.

## Como usar

Descreva o alvo com stack, funcionalidades principais e contexto de negócio. O prompt gera um plano de ataque estruturado para usar como roteiro da operação.

## Variáveis


| Variável              | Descrição                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------- |
| {{DESCRICAO_DO_ALVO}} | Stack tecnológico, funcionalidades principais, tipo de dado processado e contexto de negócio do alvo |
| {{AMBIENTE}}          | Ambiente do teste: prod / staging / código-fonte |
| {{JANELA_DE_TESTE}}   | Janela autorizada para execução dos testes |
| {{RESTRICOES}}        | Rules of Engagement: o que está fora de escopo e se testes de DoS/brute-force/upload são permitidos |


## Prompt

```
Você é um red teamer sênior de aplicações web e sistemas de IA. Com base no alvo {{DESCRICAO_DO_ALVO}}, no ambiente {{AMBIENTE}}, na janela {{JANELA_DE_TESTE}} e nas restrições {{RESTRICOES}}, elabore um plano de ataque em 5 fases:

(1) Reconhecimento: comece rodando `bootstrap-scan.sh` para o inventário automático; em seguida encadeie os prompts do Pilar 1 nesta ordem: fingerprint → superfície → rotas/SPA → integrações → package-manifest → componentes-IA → supply-chain-LLM; defina fontes de informação e o que coletar antes de qualquer teste ativo;
(2) Análise estática: quais arquivos de código priorizar, quais ferramentas SAST configurar, ordem de revisão;
(3) Análise dinâmica: fluxos críticos para testar, configuração do proxy, ordem de ataque; ajuste a agressividade conforme {{AMBIENTE}} e {{RESTRICOES}} — em prod, evite DoS e testes destrutivos sem autorização explícita;
(4) Red teaming de IA (se aplicável): componentes de LLM a atacar, técnicas e ferramentas; respeite {{AMBIENTE}} e {{RESTRICOES}} na intensidade dos testes;
(5) Relatório: estrutura de entregáveis, nível de detalhe técnico e executivo, timeline; use os prompts de `04-entregar/` para redigir os entregáveis.

Para cada fase: objetivos concretos, ferramentas específicas, entradas necessárias e saídas esperadas.
```

## Saída esperada

Plano de ataque em 5 fases com objetivos, ferramentas, entradas e saídas por fase.

## Onde usar no fluxo

Planejamento. Execute antes de iniciar qualquer auditoria para definir escopo e sequência de trabalho. Consulte `AUDITORIA.md` para o checklist completo.