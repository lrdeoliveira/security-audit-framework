# Revisão de CORS, CSRF e headers de segurança

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A05:2021 - Security Misconfiguration
**Ferramentas sugeridas:** Semgrep, manual, securityheaders.com (passivo)
**Intenção:** Auditar configuração de CORS, proteção CSRF e headers de segurança HTTP que permitem account takeover, roubo de dados cross-origin e clickjacking.

## Como usar
Cole a configuração de CORS (middleware, allowlist de origins), a estratégia de autenticação (cookie vs bearer), a proteção CSRF existente e a configuração de headers/reverse proxy.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_DE_CONFIG}} | Middleware de CORS, config de cookies/sessão, proteção CSRF e definição de headers HTTP |

## Prompt
```
Atue como especialista em segurança de configuração web. Analise {{CODIGO_DE_CONFIG}} e identifique:

(1) CORS permissivo: Access-Control-Allow-Origin com wildcard ou reflexão da origin sem allowlist, especialmente combinado com Allow-Credentials: true;
(2) CORS com allowlist fraca: regex mal escapado, match por substring/startsWith, subdomínios não confiáveis aceitos, null origin permitido;
(3) CSRF: ausência de token anti-CSRF em ações state-changing com cookie auth, SameSite ausente ou None sem justificativa, Secure/HttpOnly ausentes;
(4) Clickjacking: ausência de X-Frame-Options/frame-ancestors;
(5) Headers ausentes ou fracos: HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, cache em respostas sensíveis;
(6) Cookies de sessão: flags Secure/HttpOnly/SameSite, escopo de domínio/path muito amplo, ausência de rotação no login;
(7) Métodos HTTP e preflight: aceitação de métodos perigosos, preflight contornável.

Para cada achado: localização, cenário concreto de exploração (ex: site malicioso lendo /api/me via CORS) e a configuração corrigida.
```

## Saída esperada
Achados de CORS/CSRF/headers com cenário de exploração cross-origin e configuração corrigida pronta para aplicar.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Achados de CORS/CSRF devem ser confirmados dinamicamente no Pilar 3 (use `deriva_de`). Consulte `AUDITORIA.md` para o checklist completo.
