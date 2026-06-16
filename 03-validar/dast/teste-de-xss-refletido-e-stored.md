# Teste de XSS refletido e stored

**Pilar:** validar
**Fase:** 3
**Categoria:** dast
**OWASP:** A03:2021 - Injection
**Ferramentas sugeridas:** Burp Suite, manual, navegador com DevTools
**Intenção:** Confirmar dinamicamente XSS refletido, stored e DOM, gerando payloads que contornam o encoding/sanitização do alvo.

## Como usar
Liste os pontos de injeção candidatos (parâmetros, campos, headers, fragmentos de URL) e o contexto de renderização de cada um (HTML, atributo, JS, JSON refletido em HTML). Inclua a CSP observada, se houver.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{PONTOS_DE_INJECAO}} | Parâmetros/campos candidatos, contexto de renderização de cada um e CSP observada |

## Prompt
```
Atue como especialista em exploração de XSS. Para os pontos {{PONTOS_DE_INJECAO}}, elabore:

(1) Payloads por contexto: corpo HTML, atributo (com/sem aspas), dentro de <script>/JSON, URL/href, evento inline, CSS;
(2) Quebra de sanitização: variações que driblam allowlists e filtros comuns (case, encoding HTML/URL/unicode, tags aninhadas, mutation XSS, atributos sem valor);
(3) DOM XSS: payloads via fragmento (#), postMessage e parâmetros lidos por JS, com o sink alvo;
(4) Bypass de CSP: avaliar gadgets (JSONP, base-uri, nonce reutilizado, script-src com domínio que hospeda libs), e se a CSP realmente bloqueia o PoC;
(5) Stored XSS: onde persistir, onde renderiza (inclusive em painel admin / outro usuário) e blast radius;
(6) PoC de impacto: roubo de sessão/token, ação CSRF-via-XSS, keylogger de campo sensível — não-destrutivo.

Para cada payload: ponto de injeção, contexto, string exata, comportamento esperado se vulnerável e critério de confirmação (alert é prova de execução; descreva o impacto real).
```

## Saída esperada
Conjunto de payloads por contexto com critério de confirmação e PoC de impacto não-destrutivo.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 3 - Análise dinâmica. Confirma achados de `02-analisar/revisao-de-xss-e-seguranca-client-side.md` (use `deriva_de`). Teste stored também na ótica de quem consome o dado (admin, outro tenant). Consulte `AUDITORIA.md` para o checklist completo.
