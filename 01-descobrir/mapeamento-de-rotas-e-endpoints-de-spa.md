# Mapeamento de rotas e endpoints de SPA

**Pilar:** descobrir
**Fase:** 1
**Categoria:** recon
**OWASP:** —
**Ferramentas sugeridas:** Katana, Burp Spider
**Intenção:** Descobrir rotas client-side escondidas e endpoints de API não documentados.

## Como usar
Cole o bundle JavaScript compilado ou o arquivo de roteamento da SPA. Para apps Next.js, inclua o diretório pages/ ou app/.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{BUNDLE_OU_ROTAS}} | Bundle JavaScript compilado, arquivo de roteamento ou diretório pages/ do Next.js |

## Prompt
```
Análise {{BUNDLE_OU_ROTAS}} e extraia:

(1) Todas as rotas client-side com seus componentes e parâmetros;
(2) Chamadas de API (fetch, axios, XHR) com URL, metodo e payload;
(3) Rotas protegidas por autenticação versus abertas;
(4) Parametros dinâmicos que podem ser alvo de IDOR;
(5) Endpoints internos ou de administração não obvios;
(6) Tokens, chaves ou dados sensíveis embutidos no bundle.

Organize os resultados por nível de risco e indique o que testar primeiro no proxy.
```

## Saída esperada
Mapa de rotas com metodos HTTP, parâmetros, nível de proteção e prioridade de teste.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 1 - Reconhecimento. Combine com Katana para validar os endpoints descobertos. Consulte `AUDITORIA.md` para o checklist completo.
