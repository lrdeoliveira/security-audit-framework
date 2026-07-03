# Revisão de injection e execução arbitrária

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A03:2021 - Injection
**CWE:** CWE-89, CWE-78, CWE-94, CWE-1336, CWE-90, CWE-943
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
Atue como revisor sênior de AppSec especializado em injection. Analise {{ARQUIVO_DE_CODIGO}} linha por linha e identifique:

(1) SQL injection: concatenação direta de entrada em queries, sem parametrização;
(2) Command injection: uso de exec, spawn, system com entrada não sanitizada;
(3) Code injection: uso de eval, Function() ou exec com entrada controlável;
(4) Template injection (SSTI): interpolação direta em engines como Jinja2, Handlebars, EJS, Twig; Go `text/template` (sem escape) vs `html/template`, `Blade::render` com input;
(5) LDAP, XPath e NoSQL injection;
(6) Log injection com dados de usuário.

Sinks por linguagem:
- SQL: Go `fmt.Sprintf` em `db.Query`; PHP `DB::raw`/`whereRaw`/`DB::select("… $var")`; Node knex `.raw`/template literal; Python f-string em `cursor.execute`.
- Command: Go `exec.Command("sh","-c",…)`; PHP `exec`/`shell_exec`/`system`/`proc_open`/backticks; Node `child_process.exec` (vs `execFile`); Python `subprocess(shell=True)`/`os.system`.
- Code: Node `vm.runInContext`; Python `eval`/`exec`; PHP `eval`/`assert`/`create_function`.

Para cada achado: linha, trecho de código, explorabilidade (simples/complexa), impacto e correção mínima.
```

## Saída esperada
Lista de achados por tipo de injection com linha, trecho, explorabilidade e correção recomendada.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Use em conjunto com Semgrep (ruleset p/injection) para cobrir padrões que regras automáticas perdem. Consulte `AUDITORIA.md` para o checklist completo.
