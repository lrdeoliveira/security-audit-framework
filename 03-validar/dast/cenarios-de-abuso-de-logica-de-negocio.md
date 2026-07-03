# Cenários de abuso de lógica de negócio

**Pilar:** validar
**Fase:** 3
**Categoria:** dast
**OWASP:** A04:2021 - Insecure Design
**Ferramentas sugeridas:** Burp Suite
**Intenção:** Identificar vulnerabilidades na lógica de negócio que ferramentas automatizadas não detectam.

## Como usar
Descreva as funcionalidades de negócio com foco em fluxos financeiros, permissões, estados e transições. Quanto mais contexto, mais relevantes os cenários.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{DESCRICAO_DO_SISTEMA}} | Funcionalidades de negócio com foco em fluxos financeiros, permissões, estados e transições importantes |

## Prompt
```
Você é um especialista em abuso de lógica de negócio. Para o sistema {{DESCRICAO_DO_SISTEMA}}, identifique e elabore cenários de abuso em:

(1) Fluxos de pagamento e crédito: uso de descontos inválidos, processamento em loop, abuso de reembolso;
(2) Gerenciamento de estado: transições de estado inválidas, ressurreição de entidades deletadas;
(3) Limites e cotas: bypass de limite de uso via múltiplas contas, race conditions (single-packet attack / last-byte sync com Turbo Intruder para explorar a janela TOCTOU);
(4) Autorização contextual: operações válidas em contexto errado (ex: aprovar própria solicitação);
(5) Abuso de temporalidade: uso de tokens/vouchers após validade, janelas de tempo entre eventos;
(6) Manipulação de identidade: uso de atributos de conta de forma inesperada pela lógica do sistema.

Segurança operacional: cenários de pagamento/reembolso/crédito são destrutivos — use contas e valores de teste e confirme antes de executar.
```

## Saída esperada
Cenários de abuso com fluxo de exploração passo a passo e impacto de negócio estimado.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 3 - Análise dinâmica. Use em conjunto com revisão manual no Burp para validar os cenários identificados. Consulte `AUDITORIA.md` para o checklist completo.
