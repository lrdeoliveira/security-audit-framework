# Mapeamento de integrações e dados compartilhados

**Pilar:** descobrir
**Fase:** 1
**Categoria:** recon
**OWASP:** A05:2021 - Security Misconfiguration
**Ferramentas sugeridas:** Manual
**Intenção:** Identificar onde dados sensíveis saem do sistema e quais serviços externos tem acesso.

## Como usar
Cole o código de integração, webhooks, chamadas de API externa e configuração de serviços. Inclua variáveis de ambiente se disponíveis.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_DE_INTEGRACAO}} | Código de integrações com serviços externos, webhooks ou chamadas de API de terceiros |

## Prompt
```
Análise {{CODIGO_DE_INTEGRACAO}} e identifique:

(1) Todos os serviços externos que recebem dados do sistema;
(2) Dados enviados para cada serviço: PII, dados financeiros, tokens, conteúdo de usuário;
(3) Mecanismos de autenticação usados em cada integração: API key, OAuth, webhook secret;
(4) Ausencia de validação em webhooks recebidos;
(5) Risco de exfiltração de dados por serviço comprometido;
(6) Configurações de CORS que permitem origens desnecessarias.
```

## Saída esperada
Mapa de fluxo de dados externo com risco por integração e lacunas de autenticação identificadas.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 1 - Reconhecimento. Use para priorizar testes de supply chain e vazamento de dados. Consulte `AUDITORIA.md` para o checklist completo.
