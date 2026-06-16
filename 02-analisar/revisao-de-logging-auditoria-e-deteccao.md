# Revisão de logging, auditoria e detecção

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A09:2021 - Security Logging and Monitoring Failures
**Ferramentas sugeridas:** Semgrep, manual
**Intenção:** Verificar se eventos de segurança são registrados, se logs não vazam dados sensíveis e se há base para detecção e resposta a incidentes.

## Como usar
Cole a configuração de logging, exemplos de chamadas de log no código (auth, autorização, transações), o tratamento de erros e qualquer integração de monitoramento/alerta (SIEM, Sentry, CloudWatch).

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_DE_LOGGING}} | Config de logging, chamadas de log, tratamento de erro e integrações de observabilidade/alerta |

## Prompt
```
Atue como especialista em logging de segurança e resposta a incidentes. Analise {{CODIGO_DE_LOGGING}} e identifique:

(1) Eventos de segurança não logados: login/logout, falhas de autenticação, mudança de senha/email, falhas de autorização, uso de privilégio, mudanças de role, transações sensíveis, chamadas de tool por agentes de IA;
(2) Vazamento em logs: senhas, tokens, chaves, PII, dados de cartão, prompts/respostas de LLM com dado sensível registrados em texto claro;
(3) Log injection / forging: dados de usuário concatenados em log sem sanitização (CRLF, falsificação de entradas);
(4) Ausência de contexto para investigação: falta de timestamp UTC, request id, user id, origem (IP), correlação entre serviços;
(5) Tampering: logs graváveis pela aplicação, sem retenção/imutabilidade, sem centralização;
(6) Detecção e alerta: ausência de alarme para força bruta, picos de erro 4xx/5xx, exfiltração, anomalias de uso de IA/custo;
(7) Tratamento de erro que esconde incidentes (catch silencioso) ou que expõe stack trace ao usuário.

Para cada achado: localização, por que prejudica detecção/forense, e o que registrar (com nível e campos) sem introduzir vazamento.
```

## Saída esperada
Lista de lacunas de logging/detecção por categoria, com o evento que deveria ser registrado e os campos recomendados, sem expor dado sensível.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Complementa a análise de auth e a fase de validação: o que não é logado não é detectado. Consulte `AUDITORIA.md` para o checklist completo.
