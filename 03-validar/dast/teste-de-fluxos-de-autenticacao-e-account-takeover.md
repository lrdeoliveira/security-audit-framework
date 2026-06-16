# Teste de fluxos de autenticação e account takeover

**Pilar:** validar
**Fase:** 3
**Categoria:** dast
**OWASP:** A07:2021 - Identification and Authentication Failures
**Ferramentas sugeridas:** Burp Suite (Repeater, Intruder), manual
**Intenção:** Validar dinamicamente fluxos de autenticação — reset de senha, MFA, OAuth/OIDC, sessão — buscando caminhos de account takeover.

## Como usar
Descreva os fluxos de autenticação do alvo: registro, login, reset de senha, verificação de email, MFA e qualquer login social/SSO. Inclua exemplos de requisições e como tokens são gerados e validados.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{DESCRICAO_DOS_FLUXOS}} | Fluxos de auth com exemplos de requisição, formato de tokens, MFA e provedores de SSO/OAuth |

## Prompt
```
Atue como especialista em account takeover. Dado o contexto {{DESCRICAO_DOS_FLUXOS}}, elabore casos de teste para:

(1) Reset de senha: token previsível/curto/sem expiração, reuso de token, host header injection no link, vazamento de token via Referer, mudança de email do destinatário, falta de invalidação de sessão após reset;
(2) Verificação de email/registro: confirmação contornável, takeover por pré-registro, normalização de email (alias, unicode, case);
(3) MFA: bypass por endpoint direto, brute force de OTP sem rate-limit, reuso/janela de OTP, backup codes fracos, "remember device" forjável, downgrade de MFA;
(4) OAuth/OIDC: redirect_uri não validado, roubo de code via open redirect, state ausente (CSRF de login), confusão de provedor, account linking sem verificação, id_token com assinatura/aud/iss não validados;
(5) Sessão: fixation, ausência de rotação no login/privilege change, logout que não invalida server-side, JWT (alg none, kid injection, chave fraca, falta de exp);
(6) Credential stuffing/brute force: ausência de rate-limit/lockout, user enumeration por mensagem ou timing.

Para cada caso: requisição curl/passos, pré-condições e critério objetivo de confirmação (o que indica takeover).
```

## Saída esperada
Casos de teste de ATO por fluxo, com requisições reproduzíveis e critério de confirmação para cada um.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 3 - Análise dinâmica. Execute com pelo menos dois usuários e, para OAuth, um redirect controlado. Confirma achados de `02-analisar/revisao-de-autenticacao-e-controle-de-acesso.md` (use `deriva_de`). Consulte `AUDITORIA.md` para o checklist completo.
