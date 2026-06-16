# Revisão de injection e execução arbitraria

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A03:2021 - Injection
**Ferramentas sugeridas:** Semgrep (p/injection)
**Intenção:** Identificar injeção de SQL, comandos, código e template em arquivos de código.

## Como usar
Cole o arquivo de código a revisar. Funciona melhor arquivo por arquivo para manter o contexto focado. Priorize arquivos que lidam com entrada de usuário.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{ARQUIVO_DE_CODIGO}} | Arquivo de código-fonte a revisar: JavaScript, TypeScript, Python, Go, Java, etc. |

## Prompt
```
Atue como revisor senior de AppSec especializado em injection. Análise {{ARQUIVO_DE_CODIGO}} linha por linha e identifique:

(1) SQL injection: concatenação direta de entrada em queries, sem parametrização;
(2) Command injection: uso de exec, spawn, system com entrada não sanitizada;
(3) Code injection: uso de eval, Function() ou exec com entrada controlavel;
(4) Template injection: interpolação direta em engines como Jinja2, Handlebars, EJS;
(5) LDAP, XPath e NoSQL injection;
(6) Log injection com dados de usuário.

Para cada achado: linha, trecho de código, explorabilidade (simples/complexa), impacto e correção mínima.
```

## Saída esperada
Lista de achados por tipo de injection com linha, trecho, explorabilidade e correção recomendada.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Use em conjunto com Semgrep (ruleset p/injection) para cobrir padrões que regras automáticas perdem. Consulte `AUDITORIA.md` para o checklist completo.
