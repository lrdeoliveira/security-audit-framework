# Path traversal, SSRF e validação de entrada

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A10:2021 - SSRF
**Ferramentas sugeridas:** Semgrep, Burp (confirmação)
**Intenção:** Identificar problemas de validação que permitem acesso a recursos não autorizados.

## Como usar
Cole arquivos que processam paths de arquivo, URLs fornecidas pelo usuário ou qualquer entrada usada para acessar recursos do sistema ou rede.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_DE_ENTRADA}} | Código que processa paths, URLs externas, uploads ou qualquer entrada de usuário usada para acessar recursos |

## Prompt
```
Análise {{CODIGO_DE_ENTRADA}} como especialista em validação de entrada e identifique:

(1) Path traversal: uso de paths do usuário sem normalização (../), acesso a arquivos do sistema;
(2) SSRF: URLs do usuário em fetch/requests internos, ausência de allowlist de destinos;
(3) Open redirect: redirecionamentos com destino controlado pelo usuário sem validação;
(4) File upload: validação apenas de extensão (bypassavel), ausência de validação de conteúdo;
(5) XXE: parsing de XML sem desabilitação de entidades externas;
(6) ReDoS: expressoes regulares vulneraveis a backtracking catastrofico.

Inclua exemplos de payload para cada achado.
```

## Saída esperada
Lista de vetores com exemplos de payload de exploração e correções prioritarias.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Complemente com testes manuais no Burp para confirmar explorabilidade. Consulte `AUDITORIA.md` para o checklist completo.
