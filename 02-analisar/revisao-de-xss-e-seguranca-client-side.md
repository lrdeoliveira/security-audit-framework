# Revisão de XSS e segurança client-side

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A03:2021 - Injection
**Ferramentas sugeridas:** Semgrep, CodeQL, ESLint (eslint-plugin-security)
**Intenção:** Identificar XSS (refletido, stored e DOM), sinks perigosos e ausência de defesas client-side em SPAs e templates server-side.

## Como usar
Cole componentes de frontend (React/Vue/Angular/Svelte), templates server-side (Blade, EJS, Jinja, Razor) e a configuração de Content Security Policy. Inclua handlers de `postMessage` e qualquer renderização de HTML dinâmico.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_FRONTEND}} | Componentes de UI, templates, renderização de HTML dinâmico e configuração de CSP/headers |

## Prompt
```
Atue como especialista em segurança de aplicações client-side. Analise {{CODIGO_FRONTEND}} e identifique:

(1) XSS refletido e stored: dados de usuário renderizados sem encoding contextual (HTML, atributo, JS, URL, CSS);
(2) DOM XSS: sinks perigosos (innerHTML, outerHTML, document.write, insertAdjacentHTML, dangerouslySetInnerHTML, v-html, [innerHTML], eval, Function, setTimeout com string) alimentados por sources controláveis (location, postMessage, referrer, name); auto-escape contornado por framework: React `dangerouslySetInnerHTML`, Angular `bypassSecurityTrust*`, Svelte `{@html}`. Verifique adoção de Trusted Types;
(3) Bypass de sanitização: uso incorreto de DOMPurify/sanitizers, allowlist permissiva, sanitização no lugar errado da cadeia;
(4) Content Security Policy: ausência, uso de unsafe-inline/unsafe-eval, wildcard em script-src, nonce/hash mal aplicado;
(5) postMessage inseguro: ausência de validação de origin, handlers que confiam em event.data sem checagem;
(6) Template injection client-side e binding inseguro (Angular sandbox bypass, Vue template em dados de usuário);
(7) Outros sinks: href/src com javascript:, target=_blank sem rel=noopener, geração dinâmica de <script>; templates server-side inseguros que desligam o auto-escape: Blade `{!! $x !!}` (vs `{{ }}`), Jinja `| safe`, EJS `<%- %>`, Go `text/template` usado para HTML (vs `html/template`).

Para cada achado: localização exata (arquivo:linha), source → sink, payload de prova e correção (encoding contextual, sanitização correta, CSP).
```

## Saída esperada
Lista de sinks de XSS por arquivo com cadeia source→sink, payload de prova e correção específica por contexto.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Achados aqui geram casos para validação ativa em `03-validar/dast/teste-de-xss-refletido-e-stored.md` (preencha `deriva_de`). Consulte `AUDITORIA.md` para o checklist completo.
